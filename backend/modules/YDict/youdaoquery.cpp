#include "youdaoquery.h"
#include <QNetworkAccessManager>
#include <QUrl>
#include <QNetworkRequest>
#include <QNetworkReply>
#include <QJsonObject>
#include <QJsonDocument>
#include <QJsonParseError>
#include <QJsonArray>


YouDaoQuery::YouDaoQuery(QObject * parent):
QObject(parent)
{
	mNetworkManager = new QNetworkAccessManager(this);
	QObject::connect(mNetworkManager, SIGNAL(finished(QNetworkReply *)),
					 this, SLOT(finishedSlot(QNetworkReply *)));
}

void YouDaoQuery::finishedSlot(QNetworkReply * reply)
{
	if (reply != mReply) {
		return;
	}
	// Reading attributes of the reply
	// e.g. the HTTP status code
	QVariant statusCodeV =
		reply->attribute(QNetworkRequest::HttpStatusCodeAttribute);
	// Or the target URL if it was a redirect:
	QVariant redirectionTargetUrl =
		reply->attribute(QNetworkRequest::RedirectionTargetAttribute);
	// see CS001432 on how to handle this

	// no error received?
	if (reply->error() == QNetworkReply::NoError) {
		// read data from QNetworkReply here

		// Example 1: Creating QImage from the reply
//        QImageReader imageReader(reply);
//        QImage pic = imageReader.read();

		// Example 2: Reading bytes form the reply
		QByteArray bytes = reply->readAll();	// bytes
		QString data(bytes);	// string

		QJsonParseError error;
		QJsonDocument doc =
			QJsonDocument::fromJson(QByteArray(data.toStdString().c_str()),
									&error);
		if (error.error != QJsonParseError::NoError) {
			emit this->error();
			goto OUT;
		}
		if (doc.isObject()) {
			QJsonObject root = doc.object();
			mErrorCode = root.find("errorCdoe").value().toInt();
			mQuery = root.find("query").value().toString();
			mTranslation.clear();
			if (root.find("translation").value().isArray()) {
				QJsonArray array =
					root.find("translation").value().toArray();
				for (int i = 0; i < array.size(); i++) {
					mTranslation.append(array.at(i).toString());
				}
			}

			if (root.find("basic").value().isObject()) {
				// basic
				QJsonObject basic = root.find("basic").value().toObject();
				mPhonetic = basic.find("phonetic").value().toString();
				mUkPhonetic = basic.find("uk-phonetic").value().toString();
				mUsPhonetic = basic.find("us-phonetic").value().toString();
				mExplains.clear();
				if (basic.find("explains").value().isArray()) {
					// explains
					QJsonArray array =
						basic.find("explains").value().toArray();
					for (int i = 0; i < array.size(); i++) {
						mExplains.append(array.at(i).toString());
					}
				}
			}

		} else {
			emit this->error();
			goto OUT;
		}

		emit result();
	} else {					// Some http error received
		emit error();
	}

	// We receive ownership of the reply object
	// and therefore need to handle deletion.
  OUT:
	delete reply;
}

YouDaoQuery::~YouDaoQuery()
{
	delete mNetworkManager;
}

void YouDaoQuery::setQuery(QString words)
{
	mQuery = words;
	QString urlstr =
		QString
		("http://fanyi.youdao.com/openapi.do?keyfrom=github-wdict&key=619541059&type=data&doctype=json&version=1.1&q=").
		append(mQuery);
	QUrl url(urlstr);
	mReply = mNetworkManager->get(QNetworkRequest(url));
	// NOTE: Store QNetworkReply pointer (maybe into caller).
	// When this HTTP request is finished you will receive this same
	// QNetworkReply as response parameter.
	// By the QNetworkReply pointer you can identify request and response.
}

QString YouDaoQuery::query() const
{
	return mQuery;
}

qint32 YouDaoQuery::errorCode() const
{
	return mErrorCode;
}

QString YouDaoQuery::translation() const
{
	QString str;
	for (int i = 0; i < mTranslation.size(); i++) {
		str.append(mTranslation.at(i));
		if (i < mTranslation.size() - 1) {
			str.append(", ");
		}
	}
	return str;
}

QString YouDaoQuery::phonetic() const
{
	return mPhonetic;
}

QString YouDaoQuery::ukPhonetic() const
{
	return mUkPhonetic;
}

QString YouDaoQuery::usPhonetic() const
{
	return mUsPhonetic;
}

QString YouDaoQuery::explains() const
{
	QString str;
	for (int i = 0; i < mExplains.size(); i++) {
		str.append(mExplains.at(i));
		if (i < mExplains.size() - 1) {
			str.append("\n");
		}
	}
	return str;
}

QString YouDaoQuery::webs() const
{
	return "mWebs";
}

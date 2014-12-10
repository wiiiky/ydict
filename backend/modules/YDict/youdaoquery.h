#ifndef YOUDAOQUERY_H
#define YOUDAOQUERY_H

#include <QObject>
#include <QString>
#include <QNetworkAccessManager>
#include <QNetworkReply>
#include <QQmlListProperty>
#include <QTimer>


/*
 {
    "errorCode":0
    "query":"good",
    "translation":["好"], // 有道翻译
    "basic":{ // 有道词典-基本词典
        "phonetic":"gʊd"
        "uk-phonetic":"gʊd" //英式发音
        "us-phonetic":"ɡʊd" //美式发音
        "explains":[
            "好处",
            "好的"
            "好"
        ]
    },
    "web":[ // 有道词典-网络释义
        {
            "key":"good",

            "value":["良好","善","美好"]
        },

        {...}
    ]
}
*/

class WebTranslation:public QObject {
    Q_OBJECT public:
    explicit WebTranslation(QString _key, QList < QString > _value) {
        key = _key;
        value = _value;
    } QString key;
    QList < QString > value;
};

class YouDaoQuery:public QObject {
    Q_OBJECT

    Q_PROPERTY(QString query READ query WRITE setQuery)
    Q_PROPERTY(qint32 errorCode READ errorCode)
    Q_PROPERTY(QString translation READ translation)
    Q_PROPERTY(QString phonetic READ phonetic)
    Q_PROPERTY(QString ukPhonetic READ ukPhonetic)
    Q_PROPERTY(QString usPhonetic READ usPhonetic)
    Q_PROPERTY(QString explains READ explains)
    Q_PROPERTY(QString webs READ webs)

    Q_PROPERTY(NOTIFY error)
    Q_PROPERTY(NOTIFY result)
public:
    explicit YouDaoQuery(QObject * parent = 0);
    ~YouDaoQuery();

Q_SIGNALS:
    void error();
    void result();

private Q_SLOTS:
    void finishedSlot(QNetworkReply * reply);
    void forClipboard();
    void selectionChanged();

protected:
    void setQuery(QString words);
    QString query() const;
    qint32 errorCode() const;
    QString translation() const;
    QString phonetic() const;
    QString ukPhonetic() const;
    QString usPhonetic() const;
    QString explains() const;
    QString webs() const;

protected:
    qint32 mErrorCode;
    QString mQuery;
    QList < QString > mTranslation;
    /* basic */
    QString mPhonetic;
    QString mUkPhonetic;
    QString mUsPhonetic;
    QList < QString > mExplains;
    /* web */
    QList < WebTranslation * >mWebs;

private:
    QNetworkAccessManager * mNetworkManager;
    QNetworkReply *mReply;
};

#endif							// YOUDAOQUERY_H

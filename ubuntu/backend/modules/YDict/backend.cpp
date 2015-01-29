#include <QtQml>
#include <QtQml/QQmlContext>
#include "backend.h"
#include "youdaoquery.h"


void BackendPlugin::registerTypes(const char *uri)
{
	Q_ASSERT(uri == QLatin1String("YDict"));

//    qmlRegisterType<MyType>(uri, 1, 0, "MyType");
	qmlRegisterType < YouDaoQuery > (uri, 1, 0, "YouDaoQuery");
}

void BackendPlugin::initializeEngine(QQmlEngine * engine, const char *uri)
{
	QQmlExtensionPlugin::initializeEngine(engine, uri);
}

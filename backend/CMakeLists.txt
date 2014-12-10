include_directories(
    ${CMAKE_CURRENT_SOURCE_DIR}
)

set(
    YDictbackend_SRCS
    modules/YDict/backend.cpp
    modules/YDict/youdaoquery.cpp
)

add_library(YDictbackend MODULE
    ${YDictbackend_SRCS}
)

set_target_properties(YDictbackend PROPERTIES
         LIBRARY_OUTPUT_DIRECTORY YDict)

qt5_use_modules(YDictbackend Gui Qml Quick Core Widgets)

# Copy qmldir file to build dir for running in QtCreator
add_custom_target(YDictbackend-qmldir ALL
    COMMAND cp ${CMAKE_CURRENT_SOURCE_DIR}/modules/YDict/qmldir ${CMAKE_CURRENT_BINARY_DIR}/YDict
    DEPENDS ${QMLFILES}
)

# Install plugin file
install(TARGETS YDictbackend DESTINATION ${QT_IMPORTS_DIR}/YDict/)
install(FILES   modules/YDict/qmldir DESTINATION ${QT_IMPORTS_DIR}/YDict/)


# Генератор С++ тестов для измерения производительности С/С++ функций, описанных в формате Doxygen

## Что нужно для работы генератора

1. Уставленные python, doxygen, make. 
2. Описанные с помощью тегов Doxygen функции.
3. Сценарии производительности для каждой группы функций.
4. Шаблон сборки будущих тестов.
5. Тестируемые функции (в виде файлов с исходным кодом или библиотеки).


## Подготовка файлов с прототипами тестируемых функций

Все тестируемые функции должны быть описаны с помощью тегов Doxygen.
Использование doxygen-тега \defgroup обязательно.

## Подготовка сценария производительности

Чтобы создать сценарий производительности, нужно Doxygen-описание функции расширить специальными тегами.

Пример:

\xmlonly

        \<testperf>
	        \<param> src 		\</param> \<values>  im1 im2 \</values>
	        \<param> dst 		\</param> \<values>  im1 im2 \</values>
	        \<param> nSize 		\</param> \<values> 8 128 1024 \</values>
        \</testperf>
\endxmlonly

##### Описание тегов на основе примера

*\xmlonly* и *\endxmlonly* теги Doxygen для вставки xml-кода.

*\<testperf>* и *\</testperf>* xml-теги, которые ищет генератор для определения сценария производительности.

*\<param>* и *\</param>*  xml-теги для задания аргументов тестируемой функции.

*\<values>* и *\</values>* xml-теги для задания значений параметров функций. Функция будет протестирована с каждым из заданных значений.  

## Подготовка шаблона сборки будущего теста перед запуском генератора

Перед запуском генератора необходимо подготовить папку со следующим содержимым:
1. *Makefile*;
2. *Конфиг-файл (например: mc12101brd_nmpu0.cfg)*;
3. *main.cpp*.

##### Требования к Makefile

1. Необходимо убедиться, что *main.cpp* компилируется при вызове *make*.
2. При вызове *make run main.cpp* должен перекомпилироваться и запускаться. 
2. *Makefile* должен подключать к компиляции *main.cpp* все файлы с исходным кодом тестируемых функций.

##### Требования к main.cpp

1. В *main.cpp* обязательно должны быть подключены заголовочные файлы: *time.h, stdio.h, stdlib.h*. 
2. Должны быть подключены заголовочные файлы, необходимые для работы тестируемой функции.
3. Должны быть описаны массивы(__типа long long__) для входных и выходных данных. Их будут использовать тестируемые функции (названия массивов должны совпадать с названиями, указанными в сценарии производительности).
4. Должна быть создана главная функция *int main() { return 0; }*.


__В папке examples лежит пример подготовленного по описанным правилам проекта.__

## Описание ключей для настройки работы скрипта

### Ключ config

При заднии этого ключа скрипт будет генерировать xml-файлы описанных функций и создавать тесты производительности на основе этих xml-файлов.
В папке, из которой был вызван скрипт, появятся папки со сгененрированными тестами. Там же будет создана папка "doxy" c xml-файлами. 

При использовании этого ключа __необходимо__ передать скрипту дополнительные параметры:

1. *-i* или *--path\_to_inc* - путь к папке с файлами, в которых описаны функции в формате Doxygen.
__Этот параметр не имеет значения по умолчанию и должен быть задан обязательно.__

2. *-b* или *--path\_to_build* - путь к папке, в которой должны лежать Makefile, конфиг-файл и шаблон main.cpp.
__Этот параметр не имеет значения по умолчанию и должен быть задан обязательно.__

3. *-p* или *--point* - указывает скрипту для каких функций должны быть сгенерированны тесты (может быть равен *fixed* или *float*).
Значение по умолчанию: *float*

### Ключ run

При заднии этого ключа скрипт будет запускать сгенерированные тесты (если тесты ранее не были сгенерированы, скрипт об этом собщит).

При использовании этого ключа передать скрипту дополнительные параметры __не нужно__.

### Ключ all

При заднии этого ключа скрипт будет генерировать xml-файлы описанных функций, создавать тесты производительности на основе этих xml-файлов и запускать созданные тесты.
При использовании этого ключа __необходимо__ передать скрипту дополнительные параметры (*-i, -b* и *-p*), см. выше описание ключа config.

### Ключ outdir

При заднии этого ключа скрипт будет искать в папках со сгенерированными тестами файлы с расширениями *md* и *h* и копировать их в папку "tables". Эта папка будет создана в том месте, откуда был запущен скрипт.

При использовании этого ключа передать скрипту дополнительные параметры __не нужно__.

### Параметры для дополнительной настройки скрипта 

1. *--path\_to_tests* - путь к папке, в которой будет лежать папка(perf_tests) со сгенерированными тестами.
Значение по умолчанию: *<рабочая папка>*

2. *--path\_to_log* - путь к папке, в которой будет лежать папка(perf\_test\_log) с логами работы скрипта.
Значение по умолчанию: *<рабочая папка>*

 *<рабочая папка>* - папка, из которой запускается скрипт
 
Эти ключи могут быть использованы с любым из ключей, описанных выше.

## Запуск

Сначала нужно запустить install.bat.Этот скрипт создаст переменную окружения(с названием testperf) с путем к testperf.

#### Запуск с ключом config

*testperf config -i \<path> -b \<path>*

#### Запуск с ключом run

*testperf run*

#### Запуск с ключом all

*testperf all -i \<path> -b \<path>*

#### Запуск с ключом outdir

*testperf outdir*

Порядок задания параметров скрипта не важен. Также не обязательно задавать все параметры. Незаданные параметры будут выставлены по умолчанию.

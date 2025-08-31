#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>

#define MAX_INPUT 256
#define MAX_TASKS 6
#define FLAG "flag{test_default_flag}"

typedef struct {
    int id;
    char *title;
    char *description;
    char *expected_commands[5];
    int num_commands;
    int completed;
} Task;

Task tasks[MAX_TASKS];
int completed_tasks = 0;

void clear_screen() {
    system("clear");
}

void print_header() {
    printf("\n");
    printf("================\n");
    printf("Linux Commands Training\n");
    printf("Прогресс: %d/%d заданий выполнено\n", completed_tasks, MAX_TASKS);
    printf("================\n");
    printf("\n");
}

void create_test_environment() {
    printf("Создаем тестовую среду...\n");
    
    system("mkdir -p ~/linux_practice/documents");
    system("mkdir -p ~/linux_practice/downloads");
    system("mkdir -p ~/linux_practice/temp");
    
    system("printf 'Отлично!! Вы открыли тренировочный файл и посмотрели весь текст целиком (cat).\\n" \
           "Команда head показывает только первые строки файла. (head -n 2).\\n" \
           "Эта строка содержит слово важный для поиска через grep.\\n" \
           "Команда tail выводит последние строки файла. (tail -n 2).\\n" \
           "Команда wc -l считает количество строк в файле. (wc -l).\\n' > ~/linux_practice/documents/readme.txt");
    
    system("printf '2024-08-31 10:00:01 INFO Система запущена\\n2024-08-31 10:00:02 ERROR Ошибка подключения\\n2024-08-31 10:00:03 INFO Повторное подключение\\n2024-08-31 10:00:04 SUCCESS Подключение восстановлено\\n' > ~/linux_practice/documents/data.log");
    
    system("printf 'Старый архивный файл\\nСодержит историческую информацию\\nДата создания: 2020-01-01\\n' > ~/linux_practice/downloads/archive.txt");
    
    system("printf 'Временный файл для тестирования команд\\n' > ~/linux_practice/temp/temporary.tmp");
    
    printf("Тестовая среда создана!\n");
}

void init_tasks() {
    tasks[0].id = 1;
    tasks[0].title = "Навигация по файловой системе";
    tasks[0].description = "pwd - Показывает полный путь к текущей директории, где вы находитесь\n" \
                          "ls - Отображает список файлов и папок в текущем каталоге\n" \
                          "cd - Позволяет перейти в другую директорию\n" \
                          "ls -la - Показывает детальную информацию о файлах, включая скрытые";
    tasks[0].expected_commands[0] = "pwd";
    tasks[0].expected_commands[1] = "ls";
    tasks[0].expected_commands[2] = "cd linux_practice";
    tasks[0].expected_commands[3] = "ls -la";
    tasks[0].num_commands = 4;
    tasks[0].completed = 0;
    
    tasks[1].id = 2;
    tasks[1].title = "Работа с файлами и директориями";
    tasks[1].description = "touch - Создает пустой файл или обновляет время изменения существующего\n" \
                          "mkdir - Создает новую директорию\n" \
                          "cp - Копирует файлы или директории\n" \
                          "mv - Перемещает или переименовывает файлы и директории";
    tasks[1].expected_commands[0] = "touch test.txt";
    tasks[1].expected_commands[1] = "mkdir new_folder";
    tasks[1].expected_commands[2] = "cp test.txt new_folder/";
    tasks[1].expected_commands[3] = "mv test.txt renamed.txt";
    tasks[1].num_commands = 4;
    tasks[1].completed = 0;
    
    tasks[2].id = 3;
    tasks[2].title = "Просмотр содержимого файлов";
    tasks[2].description = "Изучите команды: cat, head, tail, wc";
    tasks[2].expected_commands[0] = "cat documents/readme.txt";
    tasks[2].expected_commands[1] = "head -n 2 documents/readme.txt";
    tasks[2].expected_commands[2] = "tail -n 2 documents/readme.txt";
    tasks[2].expected_commands[3] = "wc -l documents/readme.txt";
    tasks[2].num_commands = 4;
    tasks[2].completed = 0;
    
    tasks[3].id = 4;
    tasks[3].title = "Поиск и фильтрация";
    tasks[3].description = "find - Поиск файлов и директорий по различным критериям\n" \
                          "grep - Поиск текста внутри файлов по шаблону\n" \
                          "which - Показывает полный путь к исполняемому файлу команды";
    tasks[3].expected_commands[0] = "find . -name '*.txt'";
    tasks[3].expected_commands[1] = "grep 'важный' documents/readme.txt";
    tasks[3].expected_commands[2] = "grep 'ERROR' documents/data.log";
    tasks[3].expected_commands[3] = "which ls";
    tasks[3].num_commands = 4;
    tasks[3].completed = 0;
    
    tasks[4].id = 5;
    tasks[4].title = "Права доступа к файлам";
    tasks[4].description = "ls -l - Показывает детальную информацию о файлах, включая права доступа\n" \
                          "chmod +x - Добавляет право на выполнение файла\n" \
                          "chmod -w - Убирает право на запись в файл\n" \
                          "chmod 644 - Устанавливает конкретные права доступа в числовом виде";
    tasks[4].expected_commands[0] = "ls -l documents/readme.txt";
    tasks[4].expected_commands[1] = "chmod +x documents/readme.txt";
    tasks[4].expected_commands[2] = "chmod -w documents/readme.txt";
    tasks[4].expected_commands[3] = "chmod 644 documents/readme.txt";
    tasks[4].num_commands = 4;
    tasks[4].completed = 0;
    
    tasks[5].id = 6;
    tasks[5].title = "Процессы и система";
    tasks[5].description = "ps aux - Показывает все запущенные процессы в системе\n" \
                          "df -h - Отображает информацию об использовании дискового пространства\n" \
                          "free -h - Показывает информацию об использовании оперативной памяти\n" \
                          "head/grep - Фильтрация вывода для удобного просмотра";
    tasks[5].expected_commands[0] = "ps aux | head -5";
    tasks[5].expected_commands[1] = "df -h";
    tasks[5].expected_commands[2] = "free -h";
    tasks[5].expected_commands[3] = "ps aux | grep -v grep | head -3";
    tasks[5].num_commands = 4;
    tasks[5].completed = 0;
}

void show_task_menu() {
    printf("МЕНЮ ЗАДАНИЙ:\n");
    for (int i = 0; i < MAX_TASKS; i++) {
        char *status = tasks[i].completed ? "✓" : "○";
        printf("%d. [%s] %s\n", i + 1, status, tasks[i].title);
    }
    printf("\n");
}

int validate_command(int task_id, int step, const char *user_command) {
    char *expected = tasks[task_id].expected_commands[step];
    
    char main_cmd[50] = {0};
    char *space = strchr(expected, ' ');
    if (space) {
        strncpy(main_cmd, expected, space - expected);
    } else {
        strcpy(main_cmd, expected);
    }
    
    return (strncmp(user_command, main_cmd, strlen(main_cmd)) == 0) ||
           (strcmp(user_command, expected) == 0);
}

int execute_task(int task_id) {
    if (task_id < 0 || task_id >= MAX_TASKS) {
        return 0;
    }
    
    Task *task = &tasks[task_id];
    char input[MAX_INPUT];
    
    clear_screen();
    print_header();
    
    printf("\nЗадание %d: %s\n", task->id, task->title);
    printf("%s\n\n", task->description);
    
    chdir(getenv("HOME"));
    if (task_id >= 1) {
        chdir("linux_practice");
    }
    
    for (int step = 0; step < task->num_commands; step++) {
        printf("Шаг %d: Выполните команду: %s\n", 
               step + 1, task->expected_commands[step]);
        
        while (1) {
            printf("$ ");
            fflush(stdout);
            
            if (fgets(input, MAX_INPUT, stdin) == NULL) {
                return 0;
            }
            
            input[strcspn(input, "\n")] = 0;
            
            if (strcmp(input, "quit") == 0 || strcmp(input, "exit") == 0 || strcmp(input, "q") == 0) {
                printf("Обучение прервано. До свидания!\n");
                return 0;
            }
            
            if (validate_command(task_id, step, input)) {
                system(input);
                printf("\nУра! (＾▽＾) Все верно!\n\n");
                break;
            } else {
                printf("Ой! ( ╯︵╰ ) Попробуйте ещё раз\n");
            }
        }
    }
    
    task->completed = 1;
    completed_tasks++;

    printf("\nЗадание %d выполнено успешно!\n\n°˖✧◝( ⁰▿⁰ )◜✧˖°\n", task->id);
    getchar();
    
    return 1;
}

void show_final_flag() {
    clear_screen();
    printf("\n");
    printf("Поздравляем!(=^･ω･^=)\n");
    printf("Вы успешно выполнили все задания по Linux!\n\n");
    printf("ВАШ ФЛАГ: %s\n\n", FLAG);
    printf("Теперь вы знаете основы работы с Linux терминалом!\n\n");
}

int main() {
    init_tasks();
    create_test_environment();
    
    clear_screen();
    printf("Добро пожаловать в обучающий курс по Linux!\n");
    printf("Вас ждёт серия практических заданий, которые помогут освоить базовые команды.\n");
    printf("Выполняйте шаги последовательно: после каждой команды вы получите обратную связь.\n");
    printf("\n");
    printf("Для выхода из любого задания наберите: quit, exit или q\n");
    
    printf("\nНажмите Enter для начала обучения...");
    getchar();
    
    for (int i = 0; i < MAX_TASKS; i++) {
        if (tasks[i].completed) continue;
        
        clear_screen();
        print_header();
        show_task_menu();
        
        if (!execute_task(i)) {
            break;
        }
    }
    
    if (completed_tasks == MAX_TASKS) {
        show_final_flag();
    }
    
    return 0;
}

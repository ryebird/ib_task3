#!/usr/bin/env python3

import os
import subprocess
import sys
from pathlib import Path
import time
from rich.console import Console
from rich.panel import Panel
from rich.progress import Progress, SpinnerColumn, TextColumn
from rich.prompt import Prompt, Confirm
from rich.table import Table
from rich import print as rprint

class LinuxTrainer:
    def __init__(self):
        self.console = Console()
        self.completed_tasks = []
        self.current_task = 0
        self.total_tasks = 6
        
        self.setup_test_environment()
    
    def setup_test_environment(self):
        home = Path.home()
        practice_dir = home / "linux_practice"
        
        try:
            (practice_dir / "documents").mkdir(parents=True, exist_ok=True)
            (practice_dir / "downloads").mkdir(parents=True, exist_ok=True)
            (practice_dir / "temp").mkdir(parents=True, exist_ok=True)
            
            test_files = {
                "documents/readme.txt": "Это тестовый файл для изучения Linux команд.\nВ нем несколько строк текста.\nТретья строка содержит слово 'важный'.\nЧетвертая строка обычная.",
                "documents/data.log": "2024-08-31 10:00:01 INFO Система запущена\n2024-08-31 10:00:02 ERROR Ошибка подключения\n2024-08-31 10:00:03 INFO Повторное подключение\n2024-08-31 10:00:04 SUCCESS Подключение восстановлено",
                "downloads/archive.txt": "Старый архивный файл\nСодержит историческую информацию\nДата создания: 2020-01-01",
                "temp/temporary.tmp": "Временный файл для тестирования команд"
            }
            
            for file_path, content in test_files.items():
                full_path = practice_dir / file_path
                full_path.parent.mkdir(parents=True, exist_ok=True)
                full_path.write_text(content)
                
        except Exception as e:
            self.console.print(f"[red]Ошибка создания тестовой среды: {e}[/red]")
    
    def clear_screen(self):
        os.system('clear' if os.name == 'posix' else 'cls')
    
    def show_header(self):
        self.console.print(Panel.fit(
            "[bold cyan]🐧 Linux Commands Training 🐧[/bold cyan]\n"
            f"[green]Прогресс: {len(self.completed_tasks)}/{self.total_tasks} заданий выполнено[/green]",
            title="Добро пожаловать",
            border_style="cyan"
        ))
    
    def run_command(self, command, capture_output=True):
        try:
            if capture_output:
                result = subprocess.run(command, shell=True, capture_output=True, text=True, cwd=Path.home())
                return result.returncode == 0, result.stdout.strip(), result.stderr.strip()
            else:
                result = subprocess.run(command, shell=True, cwd=Path.home())
                return result.returncode == 0, "", ""
        except Exception as e:
            return False, "", str(e)
    
    def task_navigation(self):
        self.console.print(Panel(
            "[bold yellow]Задание 1: Навигация по файловой системе[/bold yellow]\n\n"
            "Изучите команды навигации:\n"
            "• [cyan]pwd[/cyan] - показать текущую директорию\n"
            "• [cyan]ls[/cyan] - список файлов и папок\n"
            "• [cyan]cd[/cyan] - перейти в директорию\n"
            "• [cyan]ls -la[/cyan] - детальный список с правами доступа",
            title="📁 Навигация"
        ))
        
        tasks = [
            ("Выполните команду: pwd", "pwd", lambda out: len(out) > 0),
            ("Выполните команду: ls", "ls", lambda out: "linux_practice" in out),
            ("Перейдите в папку linux_practice: cd linux_practice", "cd linux_practice && pwd", lambda out: "linux_practice" in out),
            ("Посмотрите содержимое с правами: ls -la", "ls -la", lambda out: "documents" in out and "downloads" in out)
        ]
        
        return self.execute_task_sequence(tasks)
    
    def task_files(self):
        self.console.print(Panel(
            "[bold yellow]Задание 2: Работа с файлами и директориями[/bold yellow]\n\n"
            "Изучите команды работы с файлами:\n"
            "• [cyan]touch[/cyan] - создать пустой файл\n"
            "• [cyan]mkdir[/cyan] - создать директорию\n"
            "• [cyan]cp[/cyan] - копировать файл\n"
            "• [cyan]mv[/cyan] - переместить/переименовать файл",
            title="📄 Файлы"
        ))
        
        tasks = [
            ("Создайте файл test.txt: touch test.txt", "touch test.txt && ls", lambda out: "test.txt" in out),
            ("Создайте папку new_folder: mkdir new_folder", "mkdir new_folder && ls", lambda out: "new_folder" in out),
            ("Скопируйте test.txt в new_folder: cp test.txt new_folder/", "cp test.txt new_folder/ && ls new_folder/", lambda out: "test.txt" in out),
            ("Переименуйте test.txt в renamed.txt: mv test.txt renamed.txt", "mv test.txt renamed.txt && ls", lambda out: "renamed.txt" in out and "test.txt" not in out)
        ]
        
        return self.execute_task_sequence(tasks)
    
    def task_content(self):
        self.console.print(Panel(
            "[bold yellow]Задание 3: Просмотр содержимого файлов[/bold yellow]\n\n"
            "Изучите команды для работы с содержимым:\n"
            "• [cyan]cat[/cyan] - показать весь файл\n"
            "• [cyan]head[/cyan] - показать начало файла\n"
            "• [cyan]tail[/cyan] - показать конец файла\n"
            "• [cyan]wc[/cyan] - подсчет строк, слов, символов",
            title="👁️ Содержимое"
        ))
        
        tasks = [
            ("Посмотрите содержимое файла: cat documents/readme.txt", "cat documents/readme.txt", lambda out: "тестовый файл" in out),
            ("Посмотрите первые 2 строки: head -n 2 documents/readme.txt", "head -n 2 documents/readme.txt", lambda out: out.count('\n') <= 2),
            ("Посмотрите последние 2 строки: tail -n 2 documents/readme.txt", "tail -n 2 documents/readme.txt", lambda out: "важный" in out or "обычная" in out),
            ("Подсчитайте строки в файле: wc -l documents/readme.txt", "wc -l documents/readme.txt", lambda out: "4" in out)
        ]
        
        return self.execute_task_sequence(tasks)
    
    def task_search(self):
        self.console.print(Panel(
            "[bold yellow]Задание 4: Поиск и фильтрация[/bold yellow]\n\n"
            "Изучите команды поиска:\n"
            "• [cyan]find[/cyan] - поиск файлов по параметрам\n"
            "• [cyan]grep[/cyan] - поиск текста в файлах\n"
            "• [cyan]locate[/cyan] - быстрый поиск файлов\n"
            "• [cyan]which[/cyan] - найти расположение команды",
            title="🔍 Поиск"
        ))
        
        tasks = [
            ("Найдите все .txt файлы: find . -name '*.txt'", "find . -name '*.txt'", lambda out: "readme.txt" in out),
            ("Найдите слово 'важный' в файлах: grep 'важный' documents/readme.txt", "grep 'важный' documents/readme.txt", lambda out: "важный" in out),
            ("Найдите все файлы с ERROR в логах: grep 'ERROR' documents/data.log", "grep 'ERROR' documents/data.log", lambda out: "ERROR" in out),
            ("Найдите команду python3: which python3", "which python3", lambda out: "python3" in out)
        ]
        
        return self.execute_task_sequence(tasks)
    
    def task_permissions(self):
        self.console.print(Panel(
            "[bold yellow]Задание 5: Права доступа к файлам[/bold yellow]\n\n"
            "Изучите работу с правами:\n"
            "• [cyan]chmod[/cyan] - изменить права доступа\n"
            "• [cyan]ls -l[/cyan] - посмотреть права доступа\n"
            "• [cyan]chown[/cyan] - изменить владельца (если есть права)",
            title="🔐 Права"
        ))
        
        tasks = [
            ("Посмотрите права файла: ls -l documents/readme.txt", "ls -l documents/readme.txt", lambda out: "readme.txt" in out and ("-" in out or "r" in out)),
            ("Сделайте файл исполняемым: chmod +x documents/readme.txt", "chmod +x documents/readme.txt && ls -l documents/readme.txt", lambda out: "x" in out),
            ("Уберите права на запись: chmod -w documents/readme.txt", "chmod -w documents/readme.txt && ls -l documents/readme.txt", lambda out: "readme.txt" in out),
            ("Восстановите все права: chmod 644 documents/readme.txt", "chmod 644 documents/readme.txt && ls -l documents/readme.txt", lambda out: "readme.txt" in out)
        ]
        
        return self.execute_task_sequence(tasks)
    
    def task_processes(self):
        self.console.print(Panel(
            "[bold yellow]Задание 6: Процессы и система[/bold yellow]\n\n"
            "Изучите команды системы:\n"
            "• [cyan]ps[/cyan] - список процессов\n"
            "• [cyan]top[/cyan] - мониторинг процессов\n"
            "• [cyan]df[/cyan] - использование дисков\n"
            "• [cyan]free[/cyan] - использование памяти",
            title="⚙️ Система"
        ))
        
        tasks = [
            ("Посмотрите процессы: ps aux | head -5", "ps aux | head -5", lambda out: "PID" in out or "python" in out),
            ("Посмотрите использование диска: df -h", "df -h", lambda out: "Filesystem" in out and "%" in out),
            ("Посмотрите использование памяти: free -h", "free -h", lambda out: "Mem:" in out or "total" in out),
            ("Найдите процессы python: ps aux | grep python", "ps aux | grep python", lambda out: "python" in out)
        ]
        
        return self.execute_task_sequence(tasks)
    
    def execute_task_sequence(self, tasks):
        for i, (description, expected_command, validator) in enumerate(tasks, 1):
            self.console.print(f"\n[bold]Шаг {i}:[/bold] {description}")
            
            while True:
                command = Prompt.ask("Введите команду")
                
                if command.strip().lower() in ['quit', 'exit', 'q']:
                    return False
                    
                success, output, error = self.run_command(command)
                
                if success and validator(output):
                    self.console.print("[green]✓ Правильно![/green]")
                    if output:
                        self.console.print(f"[dim]Результат: {output[:200]}{'...' if len(output) > 200 else ''}[/dim]")
                    break
                else:
                    self.console.print("[red]✗ Попробуйте еще раз.[/red]")
                    if error:
                        self.console.print(f"[red]Ошибка: {error}[/red]")
                    self.console.print(f"[yellow]Подсказка: {description}[/yellow]")
        
        return True
    
    def show_final_flag(self):
        flag = "flag{test_default_flag}"
        
        self.console.print("\n" + "="*50)
        self.console.print(Panel.fit(
            f"[bold green]🎉 ПОЗДРАВЛЯЕМ! 🎉[/bold green]\n\n"
            f"Вы успешно выполнили все задания по Linux командам!\n\n"
            f"[bold red]ВАШ ФЛАГ: {flag}[/bold red]\n\n"
            f"[dim]Теперь вы знаете основы работы с Linux терминалом![/dim]",
            title="УСПЕХ!",
            border_style="green"
        ))
        self.console.print("="*50)
    
    def main_menu(self):
        tasks = [
            ("Навигация по файловой системе", self.task_navigation),
            ("Работа с файлами и директориями", self.task_files),
            ("Просмотр содержимого файлов", self.task_content),
            ("Поиск и фильтрация", self.task_search),
            ("Права доступа к файлам", self.task_permissions),
            ("Процессы и система", self.task_processes)
        ]
        
        while len(self.completed_tasks) < self.total_tasks:
            self.clear_screen()
            self.show_header()
            
            table = Table(title="Доступные задания")
            table.add_column("№", style="cyan", width=3)
            table.add_column("Название", style="white")
            table.add_column("Статус", style="green")
            
            for i, (task_name, _) in enumerate(tasks, 1):
                status = "✓ Выполнено" if i in self.completed_tasks else "○ Не выполнено"
                style = "green" if i in self.completed_tasks else "white"
                table.add_row(str(i), task_name, status, style=style)
            
            self.console.print(table)
            
            next_task = None
            for i, (task_name, task_func) in enumerate(tasks, 1):
                if i not in self.completed_tasks:
                    next_task = (i, task_name, task_func)
                    break
            
            if next_task:
                task_num, task_name, task_func = next_task
                
                if Confirm.ask(f"\nВыполнить задание {task_num}: {task_name}?"):
                    self.console.print(f"\n[bold cyan]Начинаем задание {task_num}...[/bold cyan]")
                    
                    if task_func():
                        self.completed_tasks.append(task_num)
                        self.console.print(f"\n[bold green]✓ Задание {task_num} выполнено![/bold green]")
                    else:
                        self.console.print(f"\n[yellow]Задание {task_num} прервано.[/yellow]")
                        if not Confirm.ask("Продолжить обучение?"):
                            break
        
        if len(self.completed_tasks) == self.total_tasks:
            self.clear_screen()
            self.show_final_flag()
    
    def run(self):
        try:
            self.clear_screen()
            self.console.print(Panel.fit(
                "[bold cyan]🚀 Добро пожаловать в Linux Training! 🚀[/bold cyan]\n\n"
                "Эта программа поможет вам изучить основные команды Linux.\n"
                "Вы будете выполнять практические задания и получать мгновенную обратную связь.\n\n"
                "[yellow]Для выхода из любого задания наберите: quit, exit или q[/yellow]",
                title="Начало обучения",
                border_style="cyan"
            ))
            
            if Confirm.ask("\nГотовы начать обучение?"):
                self.main_menu()
            else:
                self.console.print("[yellow]До свидания! Возвращайтесь когда будете готовы![/yellow]")
                
        except KeyboardInterrupt:
            self.console.print("\n[yellow]Обучение прервано. До свидания![/yellow]")
        except Exception as e:
            self.console.print(f"[red]Произошла ошибка: {e}[/red]")

if __name__ == "__main__":
    trainer = LinuxTrainer()
    trainer.run()

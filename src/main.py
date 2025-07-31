from config import load_json_config
from analyzer import analyze_data
from formatter import format_report
import json
from pathlib import Path


def main():
    # Загрузка конфигурации
    config = load_json_config()

    # Анализ данных
    analysis_result = analyze_data(
        config["data_file"],
        "2023-05-20 15:30:00"
    )

    # Форматирование отчета
    report = format_report(analysis_result)  # Теперь передается правильно

    # Сохранение отчета
    report_dir = Path(config["report_dir"])
    report_dir.mkdir(exist_ok=True)

    report_path = report_dir / "report.json"
    with open(report_path, 'w', encoding='utf-8') as f:
        json.dump(report, f, indent=2, ensure_ascii=False)

    print(f"Отчет сохранен: {report_path}")


if __name__ == "__main__":
    main()
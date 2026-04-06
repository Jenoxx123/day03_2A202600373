from google_calendar_tool import book_calendar_event

my_tools = [
    # ... (giữ nguyên get_weather, calculate)
    {
        "name": "book_calendar_event",
        "description": "Dùng để đặt lịch hẹn/sự kiện vào Google Calendar. Bạn MUST truyền tham số theo đúng định dạng chuỗi: 'Tiêu đề | YYYY-MM-DDTHH:MM:SS+07:00 | YYYY-MM-DDTHH:MM:SS+07:00 | Địa điểm'. Bắt buộc dùng dấu gạch đứng '|' để ngăn cách.",
        "func": book_calendar_event
    }
]

# my_tools = [
#     {
#         "name": "get_weather",
#         "description": "Dùng để tra cứu thời tiết của một thành phố. Tham số truyền vào là tên thành phố (ví dụ: Hà Nội).",
#         "func": get_weather
#     },
#     {
#         "name": "calculate",
#         "description": "Dùng để tính toán các phép toán (+, -, *, /). Tham số truyền vào là một biểu thức (ví dụ: 30 * 2).",
#         "func": calculate
#     }
# ]
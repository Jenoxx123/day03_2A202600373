import os
from google.oauth2 import service_account
from googleapiclient.discovery import build

# Quyền truy cập API (Scope)
SCOPES = ['https://www.googleapis.com/auth/calendar.events']

# Tên file JSON của Service Account
SERVICE_ACCOUNT_FILE = 'service_account.json'

def get_calendar_service():
    """Xác thực và khởi tạo Google Calendar API bằng Service Account."""
    if not os.path.exists(SERVICE_ACCOUNT_FILE):
        raise FileNotFoundError(f"Không tìm thấy file '{SERVICE_ACCOUNT_FILE}'.")
        
    creds = service_account.Credentials.from_service_account_file(
        SERVICE_ACCOUNT_FILE, scopes=SCOPES)
        
    return build('calendar', 'v3', credentials=creds)

def book_calendar_event(args_str: str) -> str:
    """
    Hàm dành cho ReAct Agent đặt lịch.
    """
    print(f"\n[Tool Execution] Đang xử lý đặt lịch bằng Service Account: {args_str}...")
    try:
        parts = [p.strip() for p in args_str.split('|')]
        
        if len(parts) < 3:
            return "Lỗi: Không đủ tham số. Cần ít nhất 'Tiêu đề | Bắt đầu | Kết thúc'. Hãy thử lại."
        
        summary = parts[0]
        start_time = parts[1]
        end_time = parts[2]
        location = parts[3] if len(parts) > 3 else "Chưa xác định địa điểm"

        service = get_calendar_service()

        event_body = {
            'summary': summary,
            'location': location,
            'start': {
                'dateTime': start_time,
                'timeZone': 'Asia/Ho_Chi_Minh',
            },
            'end': {
                'dateTime': end_time,
                'timeZone': 'Asia/Ho_Chi_Minh',
            },
        }

        # ĐIỀN ĐỊA CHỈ EMAIL CỦA BẠN VÀO ĐÂY
        # Ví dụ: my_email = 'nguyenvana@gmail.com'
        # (Chính là email mà bạn đã dùng ở Bước 1 để share quyền cho con bot)
        MY_CALENDAR_EMAIL = 'email_cua_ban_nam_o_day@gmail.com' 

        # Gọi API tạo sự kiện thẳng vào lịch của bạn
        event_result = service.events().insert(calendarId=MY_CALENDAR_EMAIL, body=event_body).execute()
        
        return f"Thành công! Đã tạo lịch '{summary}' tại '{location}'. Link: {event_result.get('htmlLink')}"
    
    except Exception as e:
        return f"Lỗi khi gọi Google Calendar API: {str(e)}"
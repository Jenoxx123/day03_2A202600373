import os
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build

# Quyền truy cập API (Scope) - Ở đây là quyền đọc/ghi sự kiện
SCOPES = ['https://www.googleapis.com/auth/calendar.events']

def get_calendar_service():
    """Xác thực và khởi tạo Google Calendar API service."""
    creds = 'AIzaSyDx_Xw5CoIJ4Uti0x48r2n03G2sPiki_5s'
    
    # File token.json lưu trữ access và refresh tokens sau lần đăng nhập đầu tiên
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)
    
    # Nếu chưa có creds hoặc hết hạn, yêu cầu user đăng nhập lại
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            # File credentials.json bạn tải từ Google Cloud Console
            if not os.path.exists('credentials.json'):
                raise FileNotFoundError("Không tìm thấy 'credentials.json'. Hãy tải từ Google Cloud Console.")
                
            flow = InstalledAppFlow.from_client_secrets_file('credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
            
        # Lưu lại token cho những lần chạy sau
        with open('token.json', 'w') as token:
            token.write(creds.to_json())

    return build('calendar', 'v3', credentials=creds)

def book_calendar_event(args_str: str) -> str:
    """
    Hàm dành cho ReAct Agent. 
    Agent sẽ truyền vào một chuỗi cách nhau bởi dấu phẩy (hoặc dấu |).
    Format mong muốn: "Tiêu đề | Thời gian bắt đầu (ISO) | Thời gian kết thúc (ISO) | Địa điểm"
    Ví dụ: "Họp dự án AI | 2026-04-07T10:00:00+07:00 | 2026-04-07T11:00:00+07:00 | Tầng 3, Tòa nhà Vin"
    """
    print(f"\n[Tool Execution] Đang xử lý đặt lịch với dữ liệu: {args_str}...")
    try:
        # Bóc tách tham số (dùng dấu | để tránh nhầm lẫn nếu Tiêu đề/Địa điểm có dấu phẩy)
        parts = [p.strip() for p in args_str.split('|')]
        
        if len(parts) < 3:
            return "Lỗi: Không đủ tham số. Cần ít nhất 'Tiêu đề | Bắt đầu | Kết thúc'. Hãy thử lại."
        
        summary = parts[0]
        start_time = parts[1]
        end_time = parts[2]
        # Nếu có địa điểm thì lấy, không thì để trống
        location = parts[3] if len(parts) > 3 else "Chưa xác định địa điểm"

        service = get_calendar_service()

        event_body = {
            'summary': summary,
            'location': location,
            'start': {
                'dateTime': start_time,
                'timeZone': 'Asia/Ho_Chi_Minh',  # Set mặc định múi giờ VN
            },
            'end': {
                'dateTime': end_time,
                'timeZone': 'Asia/Ho_Chi_Minh',
            },
        }

        # Gọi API tạo sự kiện
        event_result = service.events().insert(calendarId='primary', body=event_body).execute()
        
        return f"Thành công! Đã tạo lịch '{summary}' tại '{location}'. Link: {event_result.get('htmlLink')}"
    
    except Exception as e:
        return f"Lỗi khi gọi Google Calendar API: {str(e)}"
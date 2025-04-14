; ------------------- Phần khai báo chung -------------------
[Setup]
; Không yêu cầu quyền admin
PrivilegesRequired=lowest

; Tên hiển thị của ứng dụng và phiên bản
AppName=LyTran TTS
AppVersion=1.0

; (QUAN TRỌNG) Hiển thị “LyTran” ở cột Publisher trong Programs & Features
AppPublisher=LyTran

; Icon hiển thị trong Programs & Features (Uninstall)
; => Bạn cần copy icon.ico vào thư mục cài đặt (xem phần [Files] bên dưới),
;    rồi đặt đường dẫn icon cho Uninstall như bên dưới.
UninstallDisplayIcon={app}\icon.ico

; Icon cho chính file cài đặt (installer)
; => File icon.ico phải ở cùng cấp hoặc bạn chỉnh đường dẫn đầy đủ.
SetupIconFile=icon.ico

; Mặc định cài vào Documents\LyTranTTS của người dùng
DefaultDirName={userdocs}\LyTranTTS

; Bật trang Directory (để người dùng có thể chọn thư mục khác nếu cần)
DisableDirPage=no

; Tên nhóm Start Menu
DefaultGroupName=LyTran TTS

; Tắt trang đặt tên nhóm shortcut
DisableProgramGroupPage=yes

; Thư mục chứa file .exe cài đặt (sau khi biên dịch)
OutputDir=dist
; Tên file cài đặt tạo ra
OutputBaseFilename=LyTranTTS-Setup

; Nén LZMA, giao diện Wizard hiện đại
Compression=lzma
SolidCompression=yes
WizardStyle=modern

; ------------------- Phần file cần copy -------------------
[Files]
; Copy file exe đã build (dist\LyTranTTS.exe) vào thư mục cài đặt
Source: "dist\app.exe"; DestDir: "{app}"; Flags: ignoreversion

; Copy icon.ico vào thư mục cài đặt (để UninstallDisplayIcon có thể tìm thấy)
Source: "icon.ico"; DestDir: "{app}"; Flags: ignoreversion

; (Nếu bạn có thêm file/thư mục khác, copy tương tự)
; Source: "dist\music\*"; DestDir: "{app}\music"; Flags: recursesubdirs createallsubdirs

; ------------------- Tạo shortcut -------------------
[Icons]
; Shortcut trong Start Menu
Name: "{group}\LyTran TTS"; Filename: "{app}\app.exe"

; Shortcut trên Desktop của user (không cần admin)
Name: "{userdesktop}\LyTran TTS"; Filename: "{app}\app.exe"; Tasks: desktopicon

; ------------------- Tạo checkbox cho shortcut Desktop -------------------
[Tasks]
Name: "desktopicon"; Description: "Tạo &shortcut trên Desktop"; GroupDescription: "Additional icons:"; Flags: unchecked

; ------------------- Chạy ứng dụng sau khi cài đặt xong -------------------
[Run]
Filename: "{app}\app.exe"; Description: "Chạy LyTran TTS"; Flags: nowait postinstall skipifsilent

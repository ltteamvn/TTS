import tkinter as tk
import customtkinter as ctk

# Một số hằng số màu và định dạng giao diện
MAIN_BG = "#FFFFFF"
BOX_BG = "#FFFFFF"
TEXT_COLOR = "#2C3E50"
ACCENT_COLOR = "#18985d"
BORDER_COLOR = "#C8E6C9"
BORDER_WIDTH = 1
CORNER_RADIUS = 10

class ScrollableComboBox(ctk.CTkFrame):
    def __init__(self, master, values, width=200, height=35,
                 default_value="Chọn giá trị", command=None,
                 corner_radius=10, border_width=1, border_color="#c8e6c9",
                 bg_color="#ffffff", text_color="#2C3E50", **kwargs):
        super().__init__(master, **kwargs)
        self.configure(width=width, height=height, fg_color=bg_color,
                       corner_radius=corner_radius, border_width=border_width,
                       border_color=border_color)
        self.pack_propagate(False)
        self.values = values
        self.command = command
        self.current_value = default_value
        self.display_button = ctk.CTkButton(self, text=self.current_value,
                                            corner_radius=(corner_radius - 2 if corner_radius >= 2 else corner_radius),
                                            fg_color=bg_color, text_color=text_color,
                                            hover_color="#f1f8e9", border_width=0,
                                            font=("Arial", 14), command=self.open_dropdown)
        self.display_button.pack(fill="both", expand=True)
        self.dropdown_window = None

    def open_dropdown(self):
        if self.dropdown_window:
            self.dropdown_window.destroy()
            self.dropdown_window = None
            return
        parent_window = self.master
        while not isinstance(parent_window, tk.Tk) and parent_window.master:
            parent_window = parent_window.master
        self.dropdown_window = tk.Toplevel(parent_window)
        self.dropdown_window.overrideredirect(True)
        self.dropdown_window.transient(parent_window)
        self.dropdown_window.grab_set()
        self.dropdown_window.lift()
        x = self.winfo_rootx()
        y = self.winfo_rooty() + self.winfo_height()
        self.dropdown_window.geometry(f"+{x}+{y}")
        self.dropdown_window.bind("<FocusOut>", lambda e: self.close_dropdown())
        parent_window.bind("<Configure>", lambda e: self.close_dropdown())
        dropdown_frame = ctk.CTkFrame(self.dropdown_window, fg_color=self.cget("fg_color"),
                                      corner_radius=self.cget("corner_radius"),
                                      border_width=self.cget("border_width"),
                                      border_color=self.cget("border_color"))
        dropdown_frame.pack()
        scroll_frame = ctk.CTkScrollableFrame(dropdown_frame, width=self.winfo_width()-2*self.cget("border_width"),
                                               height=150, fg_color=self.cget("fg_color"),
                                               corner_radius=self.cget("corner_radius"))
        scroll_frame.pack(padx=5, pady=5)
        for val in self.values:
            item_button = ctk.CTkButton(scroll_frame, text=val, corner_radius=0,
                                        fg_color=self.cget("fg_color"), text_color="#2C3E50",
                                        hover_color="#f1f8e9", command=lambda v=val: self.select_value(v))
            item_button.pack(fill="x", padx=2, pady=1)

    def close_dropdown(self):
        if self.dropdown_window:
            self.dropdown_window.destroy()
            self.dropdown_window = None

    def select_value(self, val):
        self.current_value = val
        self.display_button.configure(text=val)
        self.close_dropdown()
        if self.command:
            self.command(val)

    def get(self):
        return self.current_value

    def set(self, val):
        self.current_value = val
        self.display_button.configure(text=val)

class AudioPlayerFrame(ctk.CTkFrame):
    def __init__(self, master, width=600, height=50, **kwargs):
        super().__init__(master, width=width, height=height,
                         corner_radius=CORNER_RADIUS, border_width=BORDER_WIDTH,
                         border_color=BORDER_COLOR, **kwargs)
        self.configure(fg_color=BOX_BG)
        self.pack_propagate(False)
        self.player = None
        self.is_user_dragging = False
        self.playback_finished = False
        self.event_manager = None
        self.playback_speed = 1.0
        self.speed_menu = None
        
        control_frame = ctk.CTkFrame(self, fg_color=BOX_BG, corner_radius=CORNER_RADIUS)
        control_frame.pack(fill="both", expand=True, padx=10, pady=5)
        
        self.play_pause_btn = ctk.CTkButton(control_frame, text="▷", width=30, height=30,
                                            corner_radius=CORNER_RADIUS, fg_color="transparent",
                                            hover_color="#f1f8e9", text_color=TEXT_COLOR,
                                            font=("Arial", 16), command=self.toggle_play_pause)
        self.play_pause_btn.pack(side="left", padx=(5,8))
        
        self.time_label = ctk.CTkLabel(control_frame, text="00:00 / 00:00",
                                       font=("Arial", 12), fg_color="transparent", text_color=TEXT_COLOR)
        self.time_label.pack(side="left", padx=(0,8))
        
        self.progress_slider = ctk.CTkSlider(control_frame, from_=0, to=100,
                                             fg_color=BORDER_COLOR, button_color=ACCENT_COLOR,
                                             button_hover_color="#388E3C", command=self.on_slider_drag,
                                             width=200)
        self.progress_slider.set(0)
        self.progress_slider.pack(side="left", fill="x", expand=True, padx=(0,8))
        self.progress_slider.bind("<Button-1>", self.on_slider_click)
        self.progress_slider.bind("<ButtonRelease-1>", self.on_slider_release)
        
        volume_icon = ctk.CTkLabel(control_frame, text="🔊", font=("Arial", 14),
                                   fg_color="transparent", text_color=TEXT_COLOR)
        volume_icon.pack(side="left", padx=(0,5))
        
        self.volume_slider = ctk.CTkSlider(control_frame, from_=0, to=100, width=80,
                                           fg_color=BORDER_COLOR, button_color=ACCENT_COLOR,
                                           button_hover_color="#388E3C", command=self.set_volume)
        self.volume_slider.set(100)
        self.volume_slider.pack(side="left", padx=(0,8))
        
        self.menu_label = ctk.CTkLabel(control_frame, text="⋮", font=("Arial", 16),
                                       fg_color="transparent", text_color=TEXT_COLOR)
        self.menu_label.pack(side="left", padx=(0,5))
        self.menu_label.bind("<Button-1>", lambda e: self.open_speed_menu())
        
        self.update_loop()

    def set_volume(self, value):
        if self.player:
            self.player.audio_set_volume(int(float(value)))

    def open_speed_menu(self):
        if self.speed_menu:
            self.speed_menu.destroy()
            self.speed_menu = None
            return
        parent_window = self.master
        while not isinstance(parent_window, tk.Tk) and parent_window.master:
            parent_window = parent_window.master
        self.speed_menu = tk.Toplevel(parent_window)
        self.speed_menu.overrideredirect(True)
        self.speed_menu.transient(parent_window)
        self.speed_menu.grab_set()
        self.speed_menu.lift()
        x = self.menu_label.winfo_rootx()
        y = self.menu_label.winfo_rooty() + self.menu_label.winfo_height()
        self.speed_menu.geometry(f"+{x}+{y}")
        self.speed_menu.bind("<FocusOut>", lambda e: self.close_speed_menu())
        parent_window.bind("<Configure>", lambda e: self.close_speed_menu())
        speeds = [0.5, 0.75, 1.0, 1.25, 1.5, 2.0]
        menu_frame = ctk.CTkFrame(self.speed_menu, fg_color="#ffffff", corner_radius=6)
        menu_frame.pack(fill="both", expand=True)
        for sp in speeds:
            display_text = "Normal" if abs(sp - 1.0) < 1e-9 else str(sp)
            check_mark = " ✓" if abs(sp - self.playback_speed) < 1e-9 else ""
            btn = ctk.CTkButton(menu_frame, text=f"{display_text}{check_mark}",
                                fg_color="#ffffff", text_color="#2C3E50",
                                hover_color="#f1f8e9", corner_radius=0,
                                anchor="w", command=lambda s=sp: self.select_speed(s))
            btn.pack(fill="x", padx=5, pady=0)

    def close_speed_menu(self):
        if self.speed_menu:
            self.speed_menu.destroy()
            self.speed_menu = None

    def select_speed(self, speed_value):
        self.playback_speed = speed_value
        if self.player:
            self.player.set_rate(self.playback_speed)
        self.close_speed_menu()

    def load_file(self, file_path, autoplay=False):
        import vlc
        tts_instance = vlc.Instance()
        if self.player:
            self.player.stop()
            self.player.release()
        self.playback_finished = False
        self.player = tts_instance.media_player_new()
        media = tts_instance.media_new(file_path)
        self.player.set_media(media)
        current_volume = int(self.volume_slider.get())
        self.player.audio_set_volume(current_volume)
        self.player.play()
        self.player.set_rate(self.playback_speed)
        self.wait_for_length(autoplay)
        self.event_manager = self.player.event_manager()
        self.event_manager.event_attach(vlc.EventType.MediaPlayerEndReached, self.on_end_reached)

    def wait_for_length(self, autoplay, delay=300):
        total_len = self.player.get_length()
        if total_len <= 0:
            self.after(delay, lambda: self.wait_for_length(autoplay, delay))
        else:
            if not autoplay:
                self.player.pause()

    def on_end_reached(self, event):
        self.playback_finished = True
        total_ms = self.player.get_length()
        self.progress_slider.set(100)
        self.time_label.configure(text=f"{self.ms_to_mmss(total_ms)} / {self.ms_to_mmss(total_ms)}")
        self.play_pause_btn.configure(text="▷")

    def toggle_play_pause(self):
        if not self.player:
            return
        if self.playback_finished:
            self.player.set_time(0)
            self.playback_finished = False
        state = self.player.get_state()
        if state == vlc.State.Playing:
            self.player.pause()
            self.play_pause_btn.configure(text="▷")
        else:
            self.player.play()
            self.play_pause_btn.configure(text="❚❚")

    def on_slider_click(self, event):
        self.is_user_dragging = True

    def on_slider_release(self, event):
        self.is_user_dragging = False
        if self.player:
            total_ms = self.player.get_length()
            if total_ms > 0:
                new_time = int((self.progress_slider.get()/100)*total_ms)
                self.player.set_time(new_time)

    def on_slider_drag(self, value):
        pass

    def update_loop(self):
        if self.player:
            state = self.player.get_state()
            if state == vlc.State.Playing:
                self.play_pause_btn.configure(text="❚❚")
            else:
                if not self.playback_finished:
                    self.play_pause_btn.configure(text="▷")
            total_ms = self.player.get_length()
            current_ms = self.player.get_time()
            if self.playback_finished:
                self.progress_slider.set(100)
                self.time_label.configure(text=f"{self.ms_to_mmss(total_ms)} / {self.ms_to_mmss(total_ms)}")
            else:
                self.time_label.configure(text=f"{self.ms_to_mmss(current_ms)} / {self.ms_to_mmss(total_ms)}")
                if total_ms > 0 and not self.is_user_dragging:
                    ratio = current_ms/total_ms
                    self.progress_slider.set(min(ratio, 1.0)*100)
        self.after(500, self.update_loop)

    @staticmethod
    def ms_to_mmss(ms):
        if ms <= 0:
            return "00:00"
        seconds = ms//1000
        m = seconds//60
        s = seconds % 60
        return f"{m:01}:{s:02}"

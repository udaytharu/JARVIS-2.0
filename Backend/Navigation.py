import pyautogui
import time
import logging
from typing import Optional, Tuple
import subprocess
import os

# Configure pyautogui safety settings
pyautogui.FAILSAFE = True
pyautogui.PAUSE = 0.1

class UniversalNavigator:
    """Universal navigation class that works with almost any application"""
    
    def __init__(self):
        self.current_app = None
        self.scroll_position = 0
        self.zoom_level = 100
        
    def scroll_up(self, amount: int = 3) -> bool:
        """Scroll up in any application"""
        try:
            current_x, current_y = pyautogui.position()
            pyautogui.scroll(amount, x=current_x, y=current_y)
            self.scroll_position -= amount
            time.sleep(0.2)
            logging.info(f"Scrolled up by {amount} units at position ({current_x}, {current_y})")
            return True
        except Exception as e:
            logging.error(f"Failed to scroll up: {str(e)}")
            return False
    
    def scroll_down(self, amount: int = 3) -> bool:
        """Scroll down in any application"""
        try:
            current_x, current_y = pyautogui.position()
            pyautogui.scroll(-amount, x=current_x, y=current_y)
            self.scroll_position += amount
            time.sleep(0.2)
            logging.info(f"Scrolled down by {amount} units at position ({current_x}, {current_y})")
            return True
        except Exception as e:
            logging.error(f"Failed to scroll down: {str(e)}")
            return False
    
    def swipe_left(self, amount: int = 100) -> bool:
        """Swipe left in any application"""
        try:
            current_x, current_y = pyautogui.position()
            if current_x < amount:
                amount = current_x - 10
            pyautogui.drag(-amount, 0, duration=0.5)
            pyautogui.sleep(0.2)
            logging.info(f"Swiped left by {amount} pixels from position ({current_x}, {current_y})")
            return True
        except Exception as e:
            logging.error(f"Swipe left failed: {str(e)}")
            return False
    
    def swipe_right(self, amount: int = 100) -> bool:
        """Swipe right in any application"""
        try:
            current_x, current_y = pyautogui.position()
            screen_width, screen_height = pyautogui.size()
            if current_x + amount > screen_width:
                amount = screen_width - current_x - 10
            pyautogui.drag(amount, 0, duration=0.5)
            pyautogui.sleep(0.2)
            logging.info(f"Swiped right by {amount} pixels from position ({current_x}, {current_y})")
            return True
        except Exception as e:
            logging.error(f"Swipe right failed: {str(e)}")
            return False
    
    def swipe_up(self, amount: int = 100) -> bool:
        """Swipe up in any application"""
        try:
            current_x, current_y = pyautogui.position()
            if current_y < amount:
                amount = current_y - 10
            pyautogui.drag(0, -amount, duration=0.5)
            pyautogui.sleep(0.2)
            logging.info(f"Swiped up by {amount} pixels from position ({current_x}, {current_y})")
            return True
        except Exception as e:
            logging.error(f"Swipe up failed: {str(e)}")
            return False
    
    def swipe_down(self, amount: int = 100) -> bool:
        """Swipe down in any application"""
        try:
            current_x, current_y = pyautogui.position()
            screen_width, screen_height = pyautogui.size()
            if current_y + amount > screen_height:
                amount = screen_height - current_y - 10
            pyautogui.drag(0, amount, duration=0.5)
            pyautogui.sleep(0.2)
            logging.info(f"Swiped down by {amount} pixels from position ({current_x}, {current_y})")
            return True
        except Exception as e:
            logging.error(f"Swipe down failed: {str(e)}")
            return False
    
    def zoom_in(self) -> bool:
        """Zoom in - works in most applications"""
        try:
            pyautogui.hotkey('ctrl', 'plus')
            self.zoom_level += 10
            logging.info(f"Zoomed in to {self.zoom_level}%")
            return True
        except Exception as e:
            logging.error(f"Failed to zoom in: {str(e)}")
            return False
    
    def zoom_out(self) -> bool:
        """Zoom out - works in most applications"""
        try:
            pyautogui.hotkey('ctrl', 'minus')
            self.zoom_level = max(50, self.zoom_level - 10)
            logging.info(f"Zoomed out to {self.zoom_level}%")
            return True
        except Exception as e:
            logging.error(f"Failed to zoom out: {str(e)}")
            return False
    
    def reset_zoom(self) -> bool:
        """Reset zoom to 100%"""
        try:
            pyautogui.hotkey('ctrl', '0')
            self.zoom_level = 100
            logging.info("Reset zoom to 100%")
            return True
        except Exception as e:
            logging.error(f"Failed to reset zoom: {str(e)}")
            return False
    
    def page_up(self) -> bool:
        """Page up - works in most applications"""
        try:
            pyautogui.press('pageup')
            logging.info("Page up executed")
            return True
        except Exception as e:
            logging.error(f"Failed to page up: {str(e)}")
            return False
    
    def page_down(self) -> bool:
        """Page down - works in most applications"""
        try:
            pyautogui.press('pagedown')
            logging.info("Page down executed")
            return True
        except Exception as e:
            logging.error(f"Failed to page down: {str(e)}")
            return False
    
    def home(self) -> bool:
        """Go to home/beginning - works in most applications"""
        try:
            pyautogui.press('home')
            logging.info("Home key executed")
            return True
        except Exception as e:
            logging.error(f"Failed to go home: {str(e)}")
            return False
    
    def end(self) -> bool:
        """Go to end - works in most applications"""
        try:
            pyautogui.press('end')
            logging.info("End key executed")
            return True
        except Exception as e:
            logging.error(f"Failed to go to end: {str(e)}")
            return False
    
    def next_item(self) -> bool:
        """Next item - works in most applications"""
        try:
            pyautogui.press('right')
            logging.info("Next item executed")
            return True
        except Exception as e:
            logging.error(f"Failed to go to next item: {str(e)}")
            return False
    
    def previous_item(self) -> bool:
        """Previous item - works in most applications"""
        try:
            pyautogui.press('left')
            logging.info("Previous item executed")
            return True
        except Exception as e:
            logging.error(f"Failed to go to previous item: {str(e)}")
            return False
    
    def up_item(self) -> bool:
        """Up item - works in most applications"""
        try:
            pyautogui.press('up')
            logging.info("Up item executed")
            return True
        except Exception as e:
            logging.error(f"Failed to go up: {str(e)}")
            return False
    
    def down_item(self) -> bool:
        """Down item - works in most applications"""
        try:
            pyautogui.press('down')
            logging.info("Down item executed")
            return True
        except Exception as e:
            logging.error(f"Failed to go down: {str(e)}")
            return False
    
    def enter(self) -> bool:
        """Enter key - works in most applications"""
        try:
            pyautogui.press('enter')
            logging.info("Enter key executed")
            return True
        except Exception as e:
            logging.error(f"Failed to press enter: {str(e)}")
            return False
    
    def escape(self) -> bool:
        """Escape key - works in most applications"""
        try:
            pyautogui.press('escape')
            logging.info("Escape key executed")
            return True
        except Exception as e:
            logging.error(f"Failed to press escape: {str(e)}")
            return False
    
    def tab(self) -> bool:
        """Tab key - works in most applications"""
        try:
            pyautogui.press('tab')
            logging.info("Tab key executed")
            return True
        except Exception as e:
            logging.error(f"Failed to press tab: {str(e)}")
            return False
    
    def backspace(self) -> bool:
        """Backspace key - works in most applications"""
        try:
            pyautogui.press('backspace')
            logging.info("Backspace key executed")
            return True
        except Exception as e:
            logging.error(f"Failed to press backspace: {str(e)}")
            return False
    
    def delete(self) -> bool:
        """Delete key - works in most applications"""
        try:
            pyautogui.press('delete')
            logging.info("Delete key executed")
            return True
        except Exception as e:
            logging.error(f"Failed to press delete: {str(e)}")
            return False
    
    def select_all(self) -> bool:
        """Select all - works in most applications"""
        try:
            pyautogui.hotkey('ctrl', 'a')
            logging.info("Select all executed")
            return True
        except Exception as e:
            logging.error(f"Failed to select all: {str(e)}")
            return False
    
    def copy(self) -> bool:
        """Copy - works in most applications"""
        try:
            pyautogui.hotkey('ctrl', 'c')
            logging.info("Copy executed")
            return True
        except Exception as e:
            logging.error(f"Failed to copy: {str(e)}")
            return False
    
    def paste(self) -> bool:
        """Paste - works in most applications"""
        try:
            pyautogui.hotkey('ctrl', 'v')
            logging.info("Paste executed")
            return True
        except Exception as e:
            logging.error(f"Failed to paste: {str(e)}")
            return False
    
    def cut(self) -> bool:
        """Cut - works in most applications"""
        try:
            pyautogui.hotkey('ctrl', 'x')
            logging.info("Cut executed")
            return True
        except Exception as e:
            logging.error(f"Failed to cut: {str(e)}")
            return False
    
    def undo(self) -> bool:
        """Undo - works in most applications"""
        try:
            pyautogui.hotkey('ctrl', 'z')
            logging.info("Undo executed")
            return True
        except Exception as e:
            logging.error(f"Failed to undo: {str(e)}")
            return False
    
    def redo(self) -> bool:
        """Redo - works in most applications"""
        try:
            pyautogui.hotkey('ctrl', 'y')
            logging.info("Redo executed")
            return True
        except Exception as e:
            logging.error(f"Failed to redo: {str(e)}")
            return False
    
    def save(self) -> bool:
        """Save - works in most applications"""
        try:
            pyautogui.hotkey('ctrl', 's')
            logging.info("Save executed")
            return True
        except Exception as e:
            logging.error(f"Failed to save: {str(e)}")
            return False
    
    def open_file(self) -> bool:
        """Open file - works in most applications"""
        try:
            pyautogui.hotkey('ctrl', 'o')
            logging.info("Open file executed")
            return True
        except Exception as e:
            logging.error(f"Failed to open file: {str(e)}")
            return False
    
    def new_file(self) -> bool:
        """New file - works in most applications"""
        try:
            pyautogui.hotkey('ctrl', 'n')
            logging.info("New file executed")
            return True
        except Exception as e:
            logging.error(f"Failed to create new file: {str(e)}")
            return False
    
    def print_file(self) -> bool:
        """Print - works in most applications"""
        try:
            pyautogui.hotkey('ctrl', 'p')
            logging.info("Print executed")
            return True
        except Exception as e:
            logging.error(f"Failed to print: {str(e)}")
            return False
    
    def find(self) -> bool:
        """Find - works in most applications"""
        try:
            pyautogui.hotkey('ctrl', 'f')
            logging.info("Find executed")
            return True
        except Exception as e:
            logging.error(f"Failed to find: {str(e)}")
            return False
    
    def replace(self) -> bool:
        """Replace - works in most applications"""
        try:
            pyautogui.hotkey('ctrl', 'h')
            logging.info("Replace executed")
            return True
        except Exception as e:
            logging.error(f"Failed to replace: {str(e)}")
            return False
    
    def refresh(self) -> bool:
        """Refresh - works in most applications"""
        try:
            pyautogui.press('f5')
            logging.info("Refresh executed")
            return True
        except Exception as e:
            logging.error(f"Failed to refresh: {str(e)}")
            return False
    
    def fullscreen(self) -> bool:
        """Toggle fullscreen - works in most applications"""
        try:
            pyautogui.press('f11')
            logging.info("Fullscreen toggled")
            return True
        except Exception as e:
            logging.error(f"Failed to toggle fullscreen: {str(e)}")
            return False

# Global universal navigator instance
universal_navigator = UniversalNavigator()

# Legacy navigators for backward compatibility
class PDFNavigator:
    """Legacy PDF navigator - now uses universal navigator"""
    def __init__(self):
        self.navigator = universal_navigator
    
    def next_page(self) -> bool:
        return self.navigator.next_item()
    
    def previous_page(self) -> bool:
        return self.navigator.previous_item()
    
    def zoom_in(self) -> bool:
        return self.navigator.zoom_in()
    
    def zoom_out(self) -> bool:
        return self.navigator.zoom_out()
    
    def scroll_page_up(self, amount: int = 3) -> bool:
        return self.navigator.scroll_up(amount)
    
    def scroll_page_down(self, amount: int = 3) -> bool:
        return self.navigator.scroll_down(amount)
    
    def go_to_page(self, page_number: int) -> bool:
        try:
            pyautogui.hotkey('ctrl', 'g')
            time.sleep(0.5)
            pyautogui.write(str(page_number))
            pyautogui.press('enter')
            logging.info(f"Navigated to page {page_number}")
            return True
        except Exception as e:
            logging.error(f"Failed to go to page {page_number}: {str(e)}")
            return False

class YouTubeNavigator:
    """Legacy YouTube navigator - now uses universal navigator"""
    def __init__(self):
        self.navigator = universal_navigator
    
    def play_pause(self) -> bool:
        return self.navigator.enter()
    
    def skip_forward(self, seconds: int = 10) -> bool:
        return self.navigator.next_item()
    
    def skip_backward(self, seconds: int = 10) -> bool:
        return self.navigator.previous_item()
    
    def toggle_fullscreen(self) -> bool:
        return self.navigator.fullscreen()
    
    def volume_up(self) -> bool:
        return self.navigator.up_item()
    
    def volume_down(self) -> bool:
        return self.navigator.down_item()
    
    def next_video(self) -> bool:
        return self.navigator.next_item()
    
    def previous_video(self) -> bool:
        return self.navigator.previous_item()
    
    def scroll_feed_up(self, amount: int = 3) -> bool:
        return self.navigator.scroll_up(amount)
    
    def scroll_feed_down(self, amount: int = 3) -> bool:
        return self.navigator.scroll_down(amount)

class WebNavigator:
    """Legacy web navigator - now uses universal navigator"""
    def __init__(self):
        self.navigator = universal_navigator
    
    def scroll_page_up(self, amount: int = 3) -> bool:
        return self.navigator.scroll_up(amount)
    
    def scroll_page_down(self, amount: int = 3) -> bool:
        return self.navigator.scroll_down(amount)
    
    def refresh_page(self) -> bool:
        return self.navigator.refresh()
    
    def go_back(self) -> bool:
        try:
            pyautogui.press('alt', 'left')
            logging.info("Went back in browser history")
            return True
        except Exception as e:
            logging.error(f"Failed to go back: {str(e)}")
            return False
    
    def go_forward(self) -> bool:
        try:
            pyautogui.press('alt', 'right')
            logging.info("Went forward in browser history")
            return True
        except Exception as e:
            logging.error(f"Failed to go forward: {str(e)}")
            return False

# Global instances for backward compatibility
pdf_navigator = PDFNavigator()
youtube_navigator = YouTubeNavigator()
web_navigator = WebNavigator()

def get_navigator(app_type: str = "universal"):
    """Get universal navigator for any application"""
    return universal_navigator

# Basic Scroll and Swipe Functions (for general use)
def ScrollUp(amount: int = 3) -> bool:
    """Scroll up on the screen"""
    try:
        # Get current mouse position
        current_x, current_y = pyautogui.position()
        
        # Scroll up at current mouse position
        pyautogui.scroll(amount, x=current_x, y=current_y)
        
        # Add small delay for better user experience
        pyautogui.sleep(0.2)
        
        logging.info(f"Scrolled up by {amount} units at position ({current_x}, {current_y})")
        return True
    except Exception as e:
        logging.error(f"Scroll up failed: {str(e)}")
        return False

def ScrollDown(amount: int = 3) -> bool:
    """Scroll down on the screen"""
    try:
        # Get current mouse position
        current_x, current_y = pyautogui.position()
        
        # Scroll down at current mouse position
        pyautogui.scroll(-amount, x=current_x, y=current_y)
        
        # Add small delay for better user experience
        pyautogui.sleep(0.2)
        
        logging.info(f"Scrolled down by {amount} units at position ({current_x}, {current_y})")
        return True
    except Exception as e:
        logging.error(f"Scroll down failed: {str(e)}")
        return False

def SwipeLeft(amount: int = 100) -> bool:
    """Swipe left on the screen"""
    try:
        # Get current mouse position
        current_x, current_y = pyautogui.position()
        
        # Ensure we're not at the edge of the screen
        if current_x < amount:
            amount = current_x - 10  # Leave some margin
        
        # Perform the swipe
        pyautogui.drag(-amount, 0, duration=0.5)
        
        # Add small delay for better user experience
        pyautogui.sleep(0.2)
        
        logging.info(f"Swiped left by {amount} pixels from position ({current_x}, {current_y})")
        return True
    except Exception as e:
        logging.error(f"Swipe left failed: {str(e)}")
        return False

def SwipeRight(amount: int = 100) -> bool:
    """Swipe right on the screen"""
    try:
        # Get current mouse position
        current_x, current_y = pyautogui.position()
        
        # Get screen size to ensure we don't go off screen
        screen_width, screen_height = pyautogui.size()
        if current_x + amount > screen_width:
            amount = screen_width - current_x - 10  # Leave some margin
        
        # Perform the swipe
        pyautogui.drag(amount, 0, duration=0.5)
        
        # Add small delay for better user experience
        pyautogui.sleep(0.2)
        
        logging.info(f"Swiped right by {amount} pixels from position ({current_x}, {current_y})")
        return True
    except Exception as e:
        logging.error(f"Swipe right failed: {str(e)}")
        return False

def SwipeUp(amount: int = 100) -> bool:
    """Swipe up on the screen"""
    try:
        # Get current mouse position
        current_x, current_y = pyautogui.position()
        
        # Ensure we're not at the top of the screen
        if current_y < amount:
            amount = current_y - 10  # Leave some margin
        
        # Perform the swipe
        pyautogui.drag(0, -amount, duration=0.5)
        
        # Add small delay for better user experience
        pyautogui.sleep(0.2)
        
        logging.info(f"Swiped up by {amount} pixels from position ({current_x}, {current_y})")
        return True
    except Exception as e:
        logging.error(f"Swipe up failed: {str(e)}")
        return False

def SwipeDown(amount: int = 100) -> bool:
    """Swipe down on the screen"""
    try:
        # Get current mouse position
        current_x, current_y = pyautogui.position()
        
        # Get screen size to ensure we don't go off screen
        screen_width, screen_height = pyautogui.size()
        if current_y + amount > screen_height:
            amount = screen_height - current_y - 10  # Leave some margin
        
        # Perform the swipe
        pyautogui.drag(0, amount, duration=0.5)
        
        # Add small delay for better user experience
        pyautogui.sleep(0.2)
        
        logging.info(f"Swiped down by {amount} pixels from position ({current_x}, {current_y})")
        return True
    except Exception as e:
        logging.error(f"Swipe down failed: {str(e)}")
        return False 
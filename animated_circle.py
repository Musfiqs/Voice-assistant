"""
Animated Circle Widget for the Voice Assistant.
Creates a futuristic holographic circle with pulse and rotation animations.
"""

import math
import numpy as np
from PyQt6.QtWidgets import QWidget
from PyQt6.QtCore import QTimer, pyqtSignal, QRect
from PyQt6.QtGui import QPainter, QPen, QBrush, QColor, QRadialGradient
from config import CIRCLE_RADIUS, PULSE_SPEED, ROTATION_SPEED, PRIMARY_COLOR, ACCENT_COLOR

class AnimatedCircle(QWidget):
    # Signal emitted when circle is clicked
    circle_clicked = pyqtSignal()
    
    def __init__(self, parent=None):
        super().__init__(parent)
        
        # Animation state
        self.angle = 0.0
        self.pulse_phase = 0.0
        self.base_radius = CIRCLE_RADIUS
        self.current_radius = self.base_radius
        self.is_active = False
        self.is_listening = False
        self.is_processing = False
        
        # Colors
        self.primary_color = QColor(PRIMARY_COLOR)
        self.accent_color = QColor(ACCENT_COLOR)
        self.inactive_color = QColor("#404040")
        
        # Animation timer
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_animation)
        self.timer.start(16)  # ~60 FPS
        
        # Set widget properties
        self.setMinimumSize(300, 300)
        self.setStyleSheet("background: transparent;")
    
    def update_animation(self):
        """Update animation state and trigger repaint."""
        # Update rotation
        self.angle += ROTATION_SPEED
        if self.angle >= 360:
            self.angle = 0
        
        # Update pulse
        self.pulse_phase += PULSE_SPEED
        pulse_multiplier = 1.0 + 0.2 * math.sin(self.pulse_phase)
        
        # Different animations based on state
        if self.is_listening:
            # Faster pulse when listening
            self.current_radius = self.base_radius * (1.0 + 0.3 * math.sin(self.pulse_phase * 3))
        elif self.is_processing:
            # Steady glow when processing
            self.current_radius = self.base_radius * 1.1
        else:
            # Normal gentle pulse
            self.current_radius = self.base_radius * pulse_multiplier
        
        self.update()  # Trigger repaint
    
    def set_state(self, state):
        """Set the circle's animation state."""
        self.is_listening = (state == "listening")
        self.is_processing = (state == "processing")
        self.is_active = (state in ["listening", "processing"])
    
    def paintEvent(self, event):
        """Custom paint event to draw the animated circle."""
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        
        # Get widget center
        center_x = self.width() // 2
        center_y = self.height() // 2
        
        # Draw outer glow rings
        self._draw_glow_rings(painter, center_x, center_y)
        
        # Draw main circle
        self._draw_main_circle(painter, center_x, center_y)
        
        # Draw inner patterns
        self._draw_inner_patterns(painter, center_x, center_y)
        
        # Draw center dot
        self._draw_center_dot(painter, center_x, center_y)
    
    def _draw_glow_rings(self, painter, center_x, center_y):
        """Draw the outer glow rings."""
        if not self.is_active:
            return
        
        # Multiple glow rings with different opacities
        for i in range(3):
            ring_radius = self.current_radius + 20 + (i * 15)
            opacity = 30 - (i * 10)
            
            if self.is_listening:
                color = QColor(self.accent_color)
            else:
                color = QColor(self.primary_color)
            
            color.setAlpha(opacity)
            pen = QPen(color, 2)
            painter.setPen(pen)
            painter.setBrush(QBrush())
            
            painter.drawEllipse(
                int(center_x - ring_radius),
                int(center_y - ring_radius),
                int(ring_radius * 2),
                int(ring_radius * 2)
            )
    
    def _draw_main_circle(self, painter, center_x, center_y):
        """Draw the main circle with gradient."""
        # Create radial gradient
        gradient = QRadialGradient(center_x, center_y, self.current_radius)
        
        if self.is_listening:
            gradient.setColorAt(0, QColor(self.accent_color.red(), self.accent_color.green(), self.accent_color.blue(), 100))
            gradient.setColorAt(0.7, QColor(self.accent_color.red(), self.accent_color.green(), self.accent_color.blue(), 50))
            gradient.setColorAt(1, QColor(self.accent_color.red(), self.accent_color.green(), self.accent_color.blue(), 0))
        elif self.is_processing:
            gradient.setColorAt(0, QColor(self.primary_color.red(), self.primary_color.green(), self.primary_color.blue(), 80))
            gradient.setColorAt(0.7, QColor(self.primary_color.red(), self.primary_color.green(), self.primary_color.blue(), 40))
            gradient.setColorAt(1, QColor(self.primary_color.red(), self.primary_color.green(), self.primary_color.blue(), 0))
        else:
            gradient.setColorAt(0, QColor(self.inactive_color.red(), self.inactive_color.green(), self.inactive_color.blue(), 60))
            gradient.setColorAt(0.7, QColor(self.inactive_color.red(), self.inactive_color.green(), self.inactive_color.blue(), 30))
            gradient.setColorAt(1, QColor(self.inactive_color.red(), self.inactive_color.green(), self.inactive_color.blue(), 0))
        
        # Draw filled circle
        painter.setBrush(QBrush(gradient))
        painter.setPen(QPen())
        painter.drawEllipse(
            int(center_x - self.current_radius),
            int(center_y - self.current_radius),
            int(self.current_radius * 2),
            int(self.current_radius * 2)
        )
        
        # Draw circle outline
        if self.is_active:
            outline_color = self.accent_color if self.is_listening else self.primary_color
        else:
            outline_color = self.inactive_color
        
        pen = QPen(outline_color, 3)
        painter.setPen(pen)
        painter.setBrush(QBrush())
        painter.drawEllipse(
            int(center_x - self.current_radius),
            int(center_y - self.current_radius),
            int(self.current_radius * 2),
            int(self.current_radius * 2)
        )
    
    def _draw_inner_patterns(self, painter, center_x, center_y):
        """Draw rotating inner patterns."""
        if not self.is_active:
            return
        
        # Draw rotating triangular patterns
        pattern_color = self.accent_color if self.is_listening else self.primary_color
        pattern_color.setAlpha(150)
        pen = QPen(pattern_color, 2)
        painter.setPen(pen)
        
        # Draw 6 radial lines rotating
        for i in range(6):
            angle_rad = math.radians(self.angle + (i * 60))
            start_radius = self.current_radius * 0.3
            end_radius = self.current_radius * 0.7
            
            start_x = center_x + start_radius * math.cos(angle_rad)
            start_y = center_y + start_radius * math.sin(angle_rad)
            end_x = center_x + end_radius * math.cos(angle_rad)
            end_y = center_y + end_radius * math.sin(angle_rad)
            
            painter.drawLine(int(start_x), int(start_y), int(end_x), int(end_y))
    
    def _draw_center_dot(self, painter, center_x, center_y):
        """Draw the center activation dot."""
        dot_radius = 8
        
        if self.is_listening:
            dot_color = self.accent_color
        elif self.is_processing:
            dot_color = self.primary_color
        else:
            dot_color = self.inactive_color
        
        painter.setBrush(QBrush(dot_color))
        painter.setPen(QPen())
        painter.drawEllipse(
            int(center_x - dot_radius),
            int(center_y - dot_radius),
            int(dot_radius * 2),
            int(dot_radius * 2)
        )
    
    def mousePressEvent(self, event):
        """Handle mouse press events."""
        # Check if click is within circle bounds
        center_x = self.width() // 2
        center_y = self.height() // 2
        
        distance = math.sqrt(
            (event.position().x() - center_x) ** 2 + 
            (event.position().y() - center_y) ** 2
        )
        
        if distance <= self.current_radius:
            self.circle_clicked.emit()
        
        super().mousePressEvent(event) 
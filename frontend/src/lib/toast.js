import Toastify from 'toastify-js';
import "toastify-js/src/toastify.css";

class Toast {
    static show(message, type = 'info', duration = 3000) {
        const styles = {
            success: {
                background: "#dcfce7",
                border: "1px solid #22c55e",
                color: "#166534",
                icon: "✅"
            },
            error: {
                background: "#fee2e2",
                border: "1px solid #ef4444",
                color: "#991b1b",
                icon: "❌"
            },
            warning: {
                background: "#fef9c3",
                border: "1px solid #eab308",
                color: "#713f12",
                icon: "⚠️"
            },
            info: {
                background: "#dbeafe",
                border: "1px solid #3b82f6",
                color: "#1e3a8a",
                icon: "ℹ️"
            }
        };

        const { background, border, color, icon } = styles[type] || styles.info;

        Toastify({
            text: `${icon} ${message}`,
            duration: duration,
            gravity: 'top',
            position: 'right',
            style: {
                background,
                border,
                color,
                fontWeight: "500",
                borderRadius: "8px",
                padding: "10px 14px",
                boxShadow: "0 2px 6px rgba(0,0,0,0.08)",
                display: "flex",
                alignItems: "center",
                gap: "6px"
            },
            stopOnFocus: true,
            close: true
        }).showToast();
    }

    static success(message, duration = 3000) {
        this.show(message, 'success', duration);
    }

    static error(message, duration = 3000) {
        this.show(message, 'error', duration);
    }

    static warning(message, duration = 3000) {
        this.show(message, 'warning', duration);
    }

    static info(message, duration = 3000) {
        this.show(message, 'info', duration);
    }
}

export default Toast;

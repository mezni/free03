class Logger:
    def log(self, level: str, message: str) -> None:
        print(f"[{level.upper()}] {message}")

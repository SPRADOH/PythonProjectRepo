from telegram import Update #type:ignore
from telegram.ext import ContextTypes   #type:ignore
from db import Database
from utils import WeatherService, JokeService, format_weather_message, format_todo_message

# Initialize services
db = Database()
weather_service = WeatherService()
joke_service = JokeService()

class CommandHandlers:
    """Handles all bot commands"""
    
    @staticmethod
    async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle /start command"""
        welcome_message = (
            "👋 Welcome to MultiBot!\n\n"
            "I'm a multi-purpose bot that can help you with various tasks:\n\n"
            "📊 /weather <city> - Get weather information\n"
            "😂 /joke - Get a random joke\n"
            "📋 /todo - Show your todo list\n"
            "➕ /addtodo <task> - Add a new task\n"
            "✅ /done <id> - Mark task as completed\n"
            "🗑️ /deltodo <id> - Delete a task\n"
            "ℹ️ /help - Show this menu again"
        )
        await update.message.reply_text(welcome_message)
    
    @staticmethod
    async def help(update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle /help command"""
        help_text = (
            "📖 Available Commands:\n\n"
            "/start - Show main menu\n"
            "/help - Show this help message\n"
            "/weather <city> - Get weather for a city\n"
            "/joke - Get a random joke\n"
            "/todo - Show your todo list\n"
            "/addtodo <task> - Add a new todo task\n"
            "/done <id> - Mark todo as completed\n"
            "/deltodo <id> - Delete a todo\n"
            "/about - About this bot"
        )
        await update.message.reply_text(help_text)
    
    @staticmethod
    async def about(update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle /about command"""
        about_text = (
            "🤖 MultiBot v1.0\n\n"
            "Created as a final project using:\n"
            "• python-telegram-bot library\n"
            "• SQLite for data storage\n"
            "• OpenWeatherMap API\n"
            "• JokeAPI\n\n"
            "Developed by: [Felix Akinloye Oyediran]"
        )
        await update.message.reply_text(about_text)
    
    @staticmethod
    async def joke(update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle /joke command"""
        await update.message.reply_text("😂 Fetching a joke for you...")
        
        result = joke_service.get_joke()
        if 'error' in result:
            await update.message.reply_text(f"❌ {result['error']}")
        else:
            message = f"🎯 Category: {result['category']}\n\n{result['joke']}"
            await update.message.reply_text(message)
    
    @staticmethod
    async def weather(update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle /weather command"""
        if not context.args:
            await update.message.reply_text(
                "❌ Please provide a city name.\n"
                "Example: /weather London"
            )
            return
        
        city = " ".join(context.args)
        await update.message.reply_text(f"🌤️ Fetching weather for {city}...")
        
        result = weather_service.get_weather(city)
        message = format_weather_message(result)
        await update.message.reply_text(message)
    
    @staticmethod
    async def todo(update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle /todo command"""
        user_id = update.effective_user.id
        todos = db.get_todos(user_id)
        message = format_todo_message(todos)
        await update.message.reply_text(message)
    
    @staticmethod
    async def addtodo(update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle /addtodo command"""
        if not context.args:
            await update.message.reply_text(
                "❌ Please provide a task description.\n"
                "Example: /addtodo Buy groceries"
            )
            return
        
        user_id = update.effective_user.id
        task = " ".join(context.args)
        db.add_todo(user_id, task)
        
        await update.message.reply_text(f"✅ Task added: {task}")
    
    @staticmethod
    async def done(update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle /done command"""
        if not context.args:
            await update.message.reply_text(
                "❌ Please provide the task ID.\n"
                "Example: /done 1\n"
                "Use /todo to see task IDs"
            )
            return
        
        user_id = update.effective_user.id
        try:
            todo_id = int(context.args[0])
            if db.complete_todo(todo_id, user_id):
                await update.message.reply_text(f"✅ Task {todo_id} completed!")
            else:
                await update.message.reply_text("❌ Task not found or already completed")
        except ValueError:
            await update.message.reply_text("❌ Please provide a valid task ID")
    
    @staticmethod
    async def deltodo(update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle /deltodo command"""
        if not context.args:
            await update.message.reply_text(
                "❌ Please provide the task ID.\n"
                "Example: /deltodo 1"
            )
            return
        
        user_id = update.effective_user.id
        try:
            todo_id = int(context.args[0])
            if db.delete_todo(todo_id, user_id):
                await update.message.reply_text(f"🗑️ Task {todo_id} deleted")
            else:
                await update.message.reply_text("❌ Task not found")
        except ValueError:
            await update.message.reply_text("❌ Please provide a valid task ID")
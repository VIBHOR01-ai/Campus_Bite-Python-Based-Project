import json
import os

# ---------------- CONFIGURATION & ASSETS ----------------

# ANSI color codes for terminal styling
CLR_RESET   = "\033[0m"
CLR_BOLD    = "\033[1m"
CLR_DIM     = "\033[2m"

CLR_RED     = "\033[91m"
CLR_GREEN   = "\033[92m"
CLR_YELLOW  = "\033[93m"
CLR_BLUE    = "\033[94m"
CLR_MAGENTA = "\033[95m"
CLR_CYAN    = "\033[96m"
CLR_WHITE   = "\033[97m"

MENU = {
    "Poha": {"price": 25, "emoji": "🥣"},
    "Vada Pav": {"price": 20, "emoji": "🍔"},
    "Sandwich": {"price": 50, "emoji": "🥪"},
    "Maggi": {"price": 40, "emoji": "🍜"},
    "Samosa": {"price": 15, "emoji": "🥟"},
    "Tea": {"price": 15, "emoji": "☕"},
    "Coffee": {"price": 25, "emoji": "☕"},
    "Cold Coffee": {"price": 50, "emoji": "🧋"}
}

STATUS_BADGES = {
    "Pending": f"{CLR_YELLOW}⏳ Pending{CLR_RESET}",
    "Preparing": f"{CLR_CYAN}🍳 Preparing{CLR_RESET}",
    "Ready": f"{CLR_MAGENTA}🔔 Ready for Pickup{CLR_RESET}",
    "Completed": f"{CLR_GREEN}✅ Completed{CLR_RESET}"
}

ORDERS_FILE = "orders.json"
STUDENTS_FILE = "students.json"

STAFF_USERNAME = "staff"
STAFF_PASSWORD = "admin123"

orders = []
students = {}


# ---------------- DATA PERSISTENCE ----------------

def load_data():
    global orders, students

    if os.path.exists(ORDERS_FILE):
        try:
            with open(ORDERS_FILE, "r") as f:
                orders = json.load(f)
            if not isinstance(orders, list):
                orders = []
        except (json.JSONDecodeError, OSError):
            print(f"{CLR_RED}⚠️  Warning: Could not read orders. Starting fresh.{CLR_RESET}")
            orders = []

    if os.path.exists(STUDENTS_FILE):
        try:
            with open(STUDENTS_FILE, "r") as f:
                students = json.load(f)
            if not isinstance(students, dict):
                students = {}
        except (json.JSONDecodeError, OSError):
            print(f"{CLR_RED}⚠️  Warning: Could not read student profiles. Starting fresh.{CLR_RESET}")
            students = {}


def save_orders():
    try:
        with open(ORDERS_FILE, "w") as f:
            json.dump(orders, f, indent=4)
    except OSError:
        print(f"{CLR_RED}❌ Error: Could not save orders.{CLR_RESET}")


def save_students():
    try:
        with open(STUDENTS_FILE, "w") as f:
            json.dump(students, f, indent=4)
    except OSError:
        print(f"{CLR_RED}❌ Error: Could not save student list.{CLR_RESET}")


# ---------------- DISPLAY UTILITIES ----------------

def display_menu():
    print(f"\n{CLR_CYAN}╭──────────────────────────────────────────────────╮{CLR_RESET}")
    print(f"{CLR_CYAN}│{CLR_BOLD}{CLR_WHITE}               🍴  CAMPUSBITE MENU  🍴            {CLR_RESET}{CLR_CYAN}│{CLR_RESET}")
    print(f"{CLR_CYAN}├──────────────────────────────────────────────────┤{CLR_RESET}")
    for item, info in MENU.items():
        emoji = info["emoji"]
        price = info["price"]
        print(f"{CLR_CYAN}│{CLR_RESET}   {emoji}  {item:<25} {CLR_GREEN}₹{price:>3}{CLR_RESET}             {CLR_CYAN}│{CLR_RESET}")
    print(f"{CLR_CYAN}╰──────────────────────────────────────────────────╯{CLR_RESET}")


def show_order(order):
    order_id = order.get("order_id", "N/A")
    student = order.get("student_name", order.get("name", "Unknown"))
    student_id = order.get("student_id", "N/A")
    items = order.get("items", [])
    total = order.get("total", 0)
    raw_status = order.get("status", "Pending")
    status_display = STATUS_BADGES.get(raw_status, raw_status)

    if not items and "item" in order:
        item_summary = f"{order.get('item')} × {order.get('quantity', 1)}"
    else:
        item_summary = ", ".join(f"{it['item']} × {it['quantity']}" for it in items)

    print(f"{CLR_BOLD}📦 Order #{order_id}{CLR_RESET} [{status_display}]")
    print(f"   👤 {student} ({CLR_DIM}{student_id}{CLR_RESET})")
    print(f"   🛒 {item_summary}")
    print(f"   💰 Total: {CLR_GREEN}₹{total}{CLR_RESET}")
    print(f"{CLR_DIM}{'─' * 46}{CLR_RESET}")


# ---------------- STUDENT AUTHENTICATION ----------------

def get_or_register_student():
    while True:
        print(f"\n{CLR_BLUE}┌──────────────────────────────────────────┐{CLR_RESET}")
        print(f"{CLR_BLUE}│{CLR_BOLD}       🎓 STUDENT AUTHENTICATION 🎓       {CLR_RESET}{CLR_BLUE}│{CLR_RESET}")
        print(f"{CLR_BLUE}├──────────────────────────────────────────┤{CLR_RESET}")
        print(f"{CLR_BLUE}│{CLR_RESET}  1. 🔑 Existing Student (Enter ID)       {CLR_BLUE}│{CLR_RESET}")
        print(f"{CLR_BLUE}│{CLR_RESET}  2. 📝 Register New Student              {CLR_BLUE}│{CLR_RESET}")
        print(f"{CLR_BLUE}│{CLR_RESET}  3. ↩️  Return to Main Menu               {CLR_BLUE}│{CLR_RESET}")
        print(f"{CLR_BLUE}╰──────────────────────────────────────────╯{CLR_RESET}")

        choice = input(f"{CLR_BOLD}👉 Select (1-3): {CLR_RESET}").strip()

        if choice == "1":
            student_id = input("🔑 Enter your Student ID: ").strip().upper()
            if not student_id:
                print(f"{CLR_RED}⚠️  Student ID cannot be empty.{CLR_RESET}")
                continue

            if student_id in students:
                print(f"\n{CLR_GREEN}👋 Welcome back, {students[student_id]['name']}!{CLR_RESET}")
                return students[student_id]

            print(f"{CLR_RED}❌ Student ID not found. Please check your ID or choose option 2 to register.{CLR_RESET}")

        elif choice == "2":
            student_id = input("📝 Enter new Student ID (e.g., ST101): ").strip().upper()
            if not student_id:
                print(f"{CLR_RED}⚠️  Student ID cannot be empty.{CLR_RESET}")
                continue

            if student_id in students:
                print(f"{CLR_YELLOW}⚠️  Student ID already exists! Please use option 1 to login.{CLR_RESET}")
                continue

            name = input("👤 Enter your Full Name: ").strip()
            if not name:
                print(f"{CLR_RED}⚠️  Name cannot be empty.{CLR_RESET}")
                continue

            students[student_id] = {
                "student_id": student_id,
                "name": name
            }
            save_students()
            print(f"\n{CLR_GREEN}🎉 Registration successful! Welcome, {name}.{CLR_RESET}")
            return students[student_id]

        elif choice == "3":
            return None

        else:
            print(f"{CLR_RED}❌ Invalid selection. Please enter 1, 2, or 3.{CLR_RESET}")


# ---------------- ORDERING FLOW ----------------

def place_order(student_profile):
    cart = []
    display_menu()

    while True:
        food_choice = input(f"\n🍽️  Enter item name ({CLR_DIM}or type 'DONE' to finish{CLR_RESET}): ").strip().title()

        if food_choice.upper() == "DONE":
            if not cart:
                print(f"{CLR_YELLOW}⚠️  Cart is empty. Order cancelled.{CLR_RESET}")
                return
            break

        if food_choice not in MENU:
            print(f"{CLR_RED}⚠️  '{food_choice}' is not available. Check the menu spelling.{CLR_RESET}")
            continue

        try:
            quantity = int(input(f"🔢 Enter quantity for {food_choice}: "))
            if quantity <= 0:
                print(f"{CLR_RED}⚠️  Quantity must be at least 1.{CLR_RESET}")
                continue
        except ValueError:
            print(f"{CLR_RED}⚠️  Please enter a valid numeric quantity.{CLR_RESET}")
            continue

        price = MENU[food_choice]["price"]
        subtotal = price * quantity
        cart.append({
            "item": food_choice,
            "quantity": quantity,
            "unit_price": price,
            "subtotal": subtotal
        })
        print(f"{CLR_GREEN}✓ Added: {food_choice} × {quantity} (₹{subtotal}){CLR_RESET}")

    if orders:
        order_id = max(
            order.get("order_id", 0) for order in orders if isinstance(order, dict)
        ) + 1
    else:
        order_id = 1

    total_amount = sum(it["subtotal"] for it in cart)

    new_order = {
        "order_id": order_id,
        "student_id": student_profile.get("student_id"),
        "student_name": student_profile.get("name"),
        "items": cart,
        "total": total_amount,
        "status": "Pending"
    }

    orders.append(new_order)
    save_orders()

    # Order Receipt Card
    print(f"\n{CLR_GREEN}┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓{CLR_RESET}")
    print(f"{CLR_GREEN}┃{CLR_BOLD}{CLR_WHITE}              🧾  ORDER CONFIRMATION  🧾          {CLR_RESET}{CLR_GREEN}┃{CLR_RESET}")
    print(f"{CLR_GREEN}┣━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┫{CLR_RESET}")
    print(f"{CLR_GREEN}┃{CLR_RESET}  Order ID :#{order_id:<36}{CLR_GREEN} ┃{CLR_RESET}")
    print(f"{CLR_GREEN}┃{CLR_RESET}  Student  : {student_profile.get('name')} ({student_profile.get('student_id')}){' ' * max(0, 24 - len(student_profile.get('name')))}{CLR_GREEN}     ┃{CLR_RESET}")
    print(f"{CLR_GREEN}┣━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┫{CLR_RESET}")
    for it in cart:
        line_item = f"- {it['item']} × {it['quantity']}"
        cost = f"₹{it['subtotal']}"
        print(f"{CLR_GREEN}┃{CLR_RESET}  {line_item:<30} {cost:>14}  {CLR_GREEN} ┃{CLR_RESET}")
    print(f"{CLR_GREEN}┣━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┫{CLR_RESET}")
    print(f"{CLR_GREEN}┃{CLR_RESET}  {CLR_BOLD}Grand Total{CLR_RESET} : {CLR_GREEN}₹{total_amount:<31}{CLR_RESET}{CLR_GREEN}  ┃{CLR_RESET}")
    print(f"{CLR_GREEN}┃{CLR_RESET}  Status      : {STATUS_BADGES['Pending']:<39} {CLR_GREEN}  ┃{CLR_RESET}")
    print(f"{CLR_GREEN}┗━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┛{CLR_RESET}")


def track_order(student_profile):
    try:
        order_id = int(input("🔍 Enter Order ID to search: "))
    except ValueError:
        print(f"{CLR_RED}⚠️  Please enter a valid numeric ID.{CLR_RESET}")
        return

    for order in orders:
        if isinstance(order, dict) and order.get("order_id") == order_id:
            print(f"\n{CLR_CYAN}─── Match Found ───{CLR_RESET}")
            show_order(order)
            return

    print(f"{CLR_RED}❌ Order #{order_id} not found.{CLR_RESET}")


def view_my_orders(student_profile):
    print(f"\n{CLR_BOLD}📋 --- ORDER HISTORY FOR {student_profile.get('name', '').upper()} ({student_profile.get('student_id')}) ---{CLR_RESET}\n")
    found = False
    sid = str(student_profile.get("student_id", "")).strip().upper()
    sname = str(student_profile.get("name", "")).strip().lower()

    for order in orders:
        if isinstance(order, dict):
            order_sid = str(order.get("student_id", "")).strip().upper()
            order_sname = str(order.get("student_name", "")).strip().lower()
            if (sid and order_sid == sid) or (sname and order_sname == sname):
                show_order(order)
                found = True

    if not found:
        print(f"{CLR_YELLOW}ℹ️  No previous orders found for your account.{CLR_RESET}")


def student_panel():
    student_profile = get_or_register_student()
    if not student_profile:
        return

    while True:
        print(f"\n{CLR_CYAN}┌──────────────────────────────────────────┐{CLR_RESET}")
        print(f"{CLR_CYAN}│{CLR_BOLD}  📱 STUDENT HUB:  {student_profile['name'][:18]:<18}     {CLR_RESET}{CLR_CYAN}│{CLR_RESET}")
        print(f"{CLR_CYAN}├──────────────────────────────────────────┤{CLR_RESET}")
        print(f"{CLR_CYAN}│{CLR_RESET}  1. 📜 View Canteen Menu                 {CLR_CYAN}│{CLR_RESET}")
        print(f"{CLR_CYAN}│{CLR_RESET}  2. 🛒 Place Multi-Item Order            {CLR_CYAN}│{CLR_RESET}")
        print(f"{CLR_CYAN}│{CLR_RESET}  3. 🔍 Track an Order Status             {CLR_CYAN}│{CLR_RESET}")
        print(f"{CLR_CYAN}│{CLR_RESET}  4. 📋 View My Order History             {CLR_CYAN}│{CLR_RESET}")
        print(f"{CLR_CYAN}│{CLR_RESET}  5. 🚪 Switch Account / Logout           {CLR_CYAN}│{CLR_RESET}")
        print(f"{CLR_CYAN}╰──────────────────────────────────────────╯{CLR_RESET}")

        choice = input(f"{CLR_BOLD}👉 Option (1-5): {CLR_RESET}").strip().lower()

        if choice in ["1", "menu", "view menu", "view canteen menu"]:
            display_menu()
            input(f"\n{CLR_DIM}Press [Enter] to return to student menu...{CLR_RESET}")
        elif choice in ["2", "order", "place order"]:
            place_order(student_profile)
        elif choice in ["3", "track", "track order"]:
            track_order(student_profile)
            input(f"\n{CLR_DIM}Press [Enter] to return to student menu...{CLR_RESET}")
        elif choice in ["4", "history", "order history", "view my order history"]:
            view_my_orders(student_profile)
            input(f"\n{CLR_DIM}Press [Enter] to return to student menu...{CLR_RESET}")
        elif choice in ["5", "logout", "exit"]:
            print(f"{CLR_YELLOW}Logged out of student panel.{CLR_RESET}")
            break
        else:
            print(f"{CLR_RED}❌ Invalid selection. Please type 1, 2, 3, 4, or 5.{CLR_RESET}")


# ---------------- STAFF FEATURES ----------------

def staff_login():
    print(f"\n{CLR_MAGENTA}🔒 --- CANTEEN STAFF AUTHENTICATION ---{CLR_RESET}")
    username = input("👤 Username: ").strip()
    password = input("🔑 Password: ").strip()

    if username == STAFF_USERNAME and password == STAFF_PASSWORD:
        print(f"{CLR_GREEN}🔓 Access granted! Welcome, Staff.{CLR_RESET}")
        return True

    print(f"{CLR_RED}❌ Access denied: Invalid credentials.{CLR_RESET}")
    return False


def view_all_orders():
    print(f"\n{CLR_MAGENTA}📋 ================= ALL LIVE ORDERS ================={CLR_RESET}\n")
    if not orders:
        print(f"{CLR_DIM}No active orders registered.{CLR_RESET}")
        return

    for order in orders:
        if isinstance(order, dict):
            show_order(order)


def view_all_students():
    print(f"\n{CLR_CYAN}👥 ============= REGISTERED STUDENTS ============={CLR_RESET}")
    if not students:
        print(f"{CLR_DIM}No students registered yet.{CLR_RESET}")
        return

    for sid, info in students.items():
        print(f"🆔 {sid:<10} │ 👤 {info.get('name')}")
    print(f"{CLR_CYAN}───────────────────────────────────────────────────{CLR_RESET}")


def update_order_status():
    if not orders:
        print(f"{CLR_YELLOW}⚠️  No orders available to update.{CLR_RESET}")
        return

    try:
        order_id = int(input("🔢 Enter Order ID: "))
    except ValueError:
        print(f"{CLR_RED}⚠️  Please enter a valid numeric ID.{CLR_RESET}")
        return

    selected_order = next((o for o in orders if isinstance(o, dict) and o.get("order_id") == order_id), None)

    if not selected_order:
        print(f"{CLR_RED}❌ Order #{order_id} not found.{CLR_RESET}")
        return

    print(f"\n{CLR_BOLD}Current Status: {STATUS_BADGES.get(selected_order.get('status'), 'Unknown')}{CLR_RESET}")
    print("Update status to:")
    print("1. ⏳ Pending")
    print("2. 🍳 Preparing")
    print("3. 🔔 Ready")
    print("4. ✅ Completed")

    status_options = {
        "1": "Pending",
        "2": "Preparing",
        "3": "Ready",
        "4": "Completed"
    }

    choice = input(f"{CLR_BOLD}👉 Choice (1-4): {CLR_RESET}").strip()
    if choice in status_options:
        selected_order["status"] = status_options[choice]
        save_orders()
        print(f"{CLR_GREEN}✨ Order #{order_id} updated to '{status_options[choice]}'!{CLR_RESET}")
    else:
        print(f"{CLR_RED}❌ Invalid selection.{CLR_RESET}")


def staff_panel():
    if not staff_login():
        return

    while True:
        print(f"\n{CLR_MAGENTA}┌──────────────────────────────────────────┐{CLR_RESET}")
        print(f"{CLR_MAGENTA}│{CLR_BOLD}          🛠️  STAFF MANAGEMENT PANEL       {CLR_RESET}{CLR_MAGENTA}│{CLR_RESET}")
        print(f"{CLR_MAGENTA}├──────────────────────────────────────────┤{CLR_RESET}")
        print(f"{CLR_MAGENTA}│{CLR_RESET}  1. 📋 View All Active Orders            {CLR_MAGENTA}│{CLR_RESET}")
        print(f"{CLR_MAGENTA}│{CLR_RESET}  2. 🔄 Update Order Status               {CLR_MAGENTA}│{CLR_RESET}")
        print(f"{CLR_MAGENTA}│{CLR_RESET}  3. 👥 View Registered Students          {CLR_MAGENTA}│{CLR_RESET}")
        print(f"{CLR_MAGENTA}│{CLR_RESET}  4. ↩️  Back to Main Menu                 {CLR_MAGENTA}│{CLR_RESET}")
        print(f"{CLR_MAGENTA}╰──────────────────────────────────────────╯{CLR_RESET}")

        choice = input(f"{CLR_BOLD}👉 Option (1-4): {CLR_RESET}").strip()

        if choice == "1":
            view_all_orders()
            input(f"\n{CLR_DIM}Press [Enter] to return to staff menu...{CLR_RESET}")
        elif choice == "2":
            update_order_status()
        elif choice == "3":
            view_all_students()
            input(f"\n{CLR_DIM}Press [Enter] to return to staff menu...{CLR_RESET}")
        elif choice == "4":
            break
        else:
            print(f"{CLR_RED}❌ Invalid selection.{CLR_RESET}")


# ---------------- MAIN APPLICATION ----------------

def main():
    load_data()

    while True:
        print(f"\n{CLR_YELLOW}╔══════════════════════════════════════════╗{CLR_RESET}")
        print(f"{CLR_YELLOW}║{CLR_BOLD}{CLR_WHITE}         🍔  CAMPUSBITE SYSTEM  ☕        {CLR_RESET}{CLR_YELLOW}║{CLR_RESET}")
        print(f"{CLR_YELLOW}╠══════════════════════════════════════════╣{CLR_RESET}")
        print(f"{CLR_YELLOW}║{CLR_RESET}  1. 🎓 Student Portal (Menu / Order)     {CLR_YELLOW}║{CLR_RESET}")
        print(f"{CLR_YELLOW}║{CLR_RESET}  2. 🛠️  Staff & Kitchen Portal            {CLR_YELLOW}║{CLR_RESET}")
        print(f"{CLR_YELLOW}║{CLR_RESET}  3. ❌ Exit System                       {CLR_YELLOW}║{CLR_RESET}")
        print(f"{CLR_YELLOW}╚══════════════════════════════════════════╝{CLR_RESET}")

        choice = input(f"{CLR_BOLD}👉 Select Portal (1-3): {CLR_RESET}").strip()

        if choice == "1":
            student_panel()
        elif choice == "2":
            staff_panel()
        elif choice == "3":
            print(f"\n{CLR_CYAN}👋 Thanks for stopping by CampusBite! See you soon.{CLR_RESET}\n")
            break
        else:
            print(f"{CLR_RED}❌ Invalid choice. Please pick between 1 and 3.{CLR_RESET}")


if __name__ == "__main__":
    main()
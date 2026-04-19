import json
import os
import hashlib
import tkinter as tk
from tkinter import messagebox, simpledialog, ttk
from tkcalendar import Calendar  # Import Calendar for date selection

class BungeeJumpingManagementSystem:
    def __init__(self, root):
        self.root = root
        self.root.title("Bungee Jumping Management System")
        self.root.geometry("2560x1600")
        self.apply_theme()

        self.users_file = "users.json"
        self.bookings_file = "bookings.json"
        self.config_file = "config.json"
        self.reviews_file = "reviews.json"
        self.feedbacks_file = "feedbacks.json"
        self.load_data()
        self.create_main_menu()

    def apply_theme(self):
        # Set background and style
        self.root.configure(bg="#1E88E5")
        style = ttk.Style()
        style.theme_use('clam')  # Default theme

        # Button Styles
        style.configure('TButton', font=('Arial', 16, 'bold'), padding=25, background="#1565C0", foreground="white", borderwidth=0)
        style.map('TButton', background=[('active', '#42A5F5')], foreground=[('active', 'white')])

        # Label Styles
        style.configure('TLabel', background="#1E88E5", font=('Arial', 18, 'bold'), foreground="#FFFFFF")

        # Frame Styles
        style.configure('TFrame', background="#1E88E5")

        # Entry Styles
        style.configure('TEntry', font=('Arial', 16), padding=5)

    def load_data(self):
        self.users = self.load_file(self.users_file, {})
        self.bookings = self.load_file(self.bookings_file, [])
        config = self.load_file(self.config_file, {"price": 100, "discount": 0, "locations": {}})
        self.price = config.get("price", 100)
        self.discount = config.get("discount", 0)
        self.locations = config.get("locations", {
            "Location A": {"slots": 5, "timings": "9 AM - 11 AM"},
            "Location B": {"slots": 5, "timings": "1 PM - 3 PM"},
            "Location C": {"slots": 5, "timings": "4 PM - 6 PM"}
        })
        self.reviews = self.load_file(self.reviews_file, [])
        self.feedbacks = self.load_file(self.feedbacks_file, [])
        self.admin_password_hash = self.hash_password("admin123")

    def save_data(self):
        self.save_file(self.users_file, self.users)
        self.save_file(self.bookings_file, self.bookings)
        self.save_file(self.config_file, {"price": self.price, "discount": self.discount, "locations": self.locations})
        self.save_file(self.reviews_file, self.reviews)
        self.save_file(self.feedbacks_file, self.feedbacks)

    def load_file(self, filename, default):
        if os.path.exists(filename):
            try:
                with open(filename, 'r') as file:
                    return json.load(file)
            except json.JSONDecodeError:
                messagebox.showerror("Error", f"Error loading {filename}. Using default values.")
        return default

    def save_file(self, filename, data):
        try:
            with open(filename, 'w') as file:
                json.dump(data, file, indent=4)
        except IOError:
            messagebox.showerror("Error", f"Error saving {filename}.")

    def hash_password(self, password):
        return hashlib.sha256(password.encode()).hexdigest()

    def verify_password(self, stored_hash, provided_password):
        return stored_hash == self.hash_password(provided_password)

    def create_main_menu(self):
        # Main Menu
        main_frame = ttk.Frame(self.root)
        main_frame.pack(pady=40)

        ttk.Label(main_frame, text="Bunjee Jumping Management System", font=("Monotype Corsiva", 46, 'bold','italic')).pack(pady=10)
        self.admin_login_button = ttk.Button(main_frame, text="Admin", command=self.admin_login)
        self.admin_login_button.pack(pady=10, fill='x')

        self.user_login_button = ttk.Button(main_frame, text="User", command=self.user_login)
        self.user_login_button.pack(pady=10, fill='x')

        self.register_button = ttk.Button(main_frame, text="Register", command=self.register_user)
        self.register_button.pack(pady=10, fill='x')

        ttk.Button(main_frame, text="Safety Measures and Terms", command=self.show_safety_measures).pack(pady=10, fill='x')

        

        ttk.Button(main_frame, text="Exit", command=self.root.quit).pack(pady=20, fill='x')

    # Admin Interface
    def admin_login(self):
        password = simpledialog.askstring("Admin Login", "Enter admin password:", show='*')
        if password is None:
            return  # User cancelled
        if not self.verify_password(self.admin_password_hash, password):
            messagebox.showerror("Error", "Incorrect password!")
            return
        self.admin_menu()

    def admin_menu(self):
        admin_window = tk.Toplevel(self.root)
        admin_window.title("Admin Menu")
        admin_window.geometry("2560x1600")

        admin_frame = ttk.Frame(admin_window)
        admin_frame.pack(pady=20)

        ttk.Label(admin_frame, text="Admin Menu", font=("Arial", 24, 'bold')).pack(pady=10)

        ttk.Button(admin_frame, text="View Bookings", command=self.view_bookings).pack(pady=5, fill='x')
        ttk.Button(admin_frame, text="Adjust Price", command=self.adjust_price).pack(pady=5, fill='x')
        ttk.Button(admin_frame, text="Set Discount", command=self.set_discount).pack(pady=5, fill='x')
        ttk.Button(admin_frame, text="View Locations", command=self.view_locations).pack(pady=5, fill='x')
        ttk.Button(admin_frame, text="Cancel Booking", command=self.admin_cancel_booking).pack(pady=5, fill='x')
        ttk.Button(admin_frame, text="Add Location", command=self.add_location).pack(pady=5, fill='x')
        ttk.Button(admin_frame, text="Update Slots", command=self.update_slots).pack(pady=5, fill='x')
        ttk.Button(admin_frame, text="Exit", command=admin_window.destroy).pack(pady=10, fill='x')

    # View and adjust admin options
    def view_bookings(self):
        bookings_window = tk.Toplevel(self.root)
        bookings_window.title("View Bookings")
        bookings_window.geometry("2560x1600")  # Adjusted for better visibility

        bookings_frame = ttk.Frame(bookings_window)
        bookings_frame.pack(pady=10, fill='both', expand=True)

        ttk.Label(bookings_frame, text="All Bookings", font=("Arial", 20, 'bold')).pack(pady=5)

        if not self.bookings:
            ttk.Label(bookings_frame, text="No bookings yet.", font=("Arial", 16)).pack()
        else:
        # Adding a scrollbar for better navigation if there are many bookings
            canvas = tk.Canvas(bookings_frame)
            scrollbar = ttk.Scrollbar(bookings_frame, orient="vertical", command=canvas.yview)
            scrollable_frame = ttk.Frame(canvas)

            scrollable_frame.bind(
                "<Configure>",
                lambda e: canvas.configure(
                    scrollregion=canvas.bbox("all")
                )
            )

            canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
            canvas.configure(yscrollcommand=scrollbar.set)

            canvas.pack(side="left", fill="both", expand=True)
            scrollbar.pack(side="right", fill="y")

        # Use a consistent font size and alignment
            for booking in self.bookings:
                booking_text = (
                    f"Username: {booking.get('username', 'N/A')} | "
                    f"Location: {booking.get('location', 'N/A')} | "
                    f"Date: {booking.get('date', 'N/A')} | "
                    f"Time: {booking.get('time', 'N/A')} | "
                    f"Price: ₹{booking.get('price', 0):.2f}"
                )
                ttk.Label(scrollable_frame, text=booking_text, font=("Arial", 10)).pack(pady=2, anchor='w')

    # Adding an Exit button
        ttk.Button(bookings_frame, text="Exit", command=bookings_window.destroy).pack(pady=10)

    def adjust_price(self):
        new_price = simpledialog.askfloat("Adjust Price", "Enter new price:", minvalue=0.01)
        if new_price is not None:
            self.price = new_price
            self.save_data()
            messagebox.showinfo("Success", f"Price adjusted to ₹{self.price:.2f}")
        else:
            messagebox.showerror("Error", "Invalid price entered.")

    def set_discount(self):
        new_discount = simpledialog.askfloat("Set Discount", "Enter discount percentage (0-100):", minvalue=0, maxvalue=100)
        if new_discount is not None:
            self.discount = new_discount
            self.save_data()
            messagebox.showinfo("Success", f"Discount set to {self.discount}%")
        else:
            messagebox.showerror("Error", "Invalid discount entered.")


    def view_locations(self):
        locations_window = tk.Toplevel(self.root)
        locations_window.title("View Locations")
        locations_window.geometry("2560x1600")  # Adjusted for a standard viewable size

        locations_frame = ttk.Frame(locations_window)
        locations_frame.pack(pady=10, fill="both", expand=True)

        ttk.Label(locations_frame, text="Available Locations", font=("Arial", 20, 'bold')).pack(pady=5)

        if not self.locations:
            ttk.Label(locations_frame, text="No locations available.", font=("Arial", 16)).pack()
        else:
            # Create a canvas for both horizontal and vertical scrolling
            canvas = tk.Canvas(locations_frame)
            h_scrollbar = ttk.Scrollbar(locations_frame, orient="horizontal", command=canvas.xview)
            v_scrollbar = ttk.Scrollbar(locations_frame, orient="vertical", command=canvas.yview)

            scrollable_frame = ttk.Frame(canvas)

            # Update scrollable area
            scrollable_frame.bind(
                "<Configure>",
                lambda e: canvas.configure(
                    scrollregion=canvas.bbox("all")
                )
            )

            # Place the frame in the canvas
            canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
            canvas.configure(xscrollcommand=h_scrollbar.set, yscrollcommand=v_scrollbar.set)

            canvas.pack(side="left", fill="both", expand=True)
            h_scrollbar.pack(side="bottom", fill="x")
            v_scrollbar.pack(side="right", fill="y")

            # Display each location information
            for loc_name, loc_info in self.locations.items():
                location_text = (
                    f"Location: {loc_name}, "
                    f"Timings: {loc_info.get('timings', 'N/A')}, "
                    f"Slots: {loc_info.get('slots', 'N/A')}"
                )
                ttk.Label(scrollable_frame, text=location_text, font=("Arial", 16)).pack(pady=2, anchor='w')

        # Add the Exit button
        exit_button = ttk.Button(locations_window, text="Exit", command=locations_window.destroy)
        exit_button.pack(pady=10)

    def admin_cancel_booking(self):
        cancel_window = tk.Toplevel(self.root)
        cancel_window.title("Cancel Booking")
        cancel_window.geometry("2560x1600")  # Standard size for easy viewing

        # Main frame and canvas for scrolling content
        main_frame = ttk.Frame(cancel_window)
        main_frame.pack(fill="both", expand=True)

        # Canvas for scrollable content
        canvas = tk.Canvas(main_frame)
        canvas.pack(side="left", fill="both", expand=True)

        # Scrollbars for vertical and horizontal scrolling
        vertical_scroll = ttk.Scrollbar(main_frame, orient="vertical", command=canvas.yview)
        horizontal_scroll = ttk.Scrollbar(main_frame, orient="horizontal", command=canvas.xview)
        vertical_scroll.pack(side="right", fill="y")
        horizontal_scroll.pack(side="bottom", fill="x")
        canvas.configure(yscrollcommand=vertical_scroll.set, xscrollcommand=horizontal_scroll.set)

        # Frame inside canvas to hold booking information
        scrollable_frame = ttk.Frame(canvas)

        # Bind scrollable area
        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )

        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")

        # Page Title
        ttk.Label(scrollable_frame, text="All Bookings", font=("Arial", 16, 'bold')).pack(pady=5)

        # If no bookings, show message
        if not self.bookings:
            ttk.Label(scrollable_frame, text="No bookings found.", font=("Arial", 12)).pack(pady=5)
        else:
            for booking in self.bookings:
                # Booking details with smaller font and compact layout
                location = booking.get('location', 'N/A')
                date = booking.get('date', 'N/A')
                time = booking.get('time', 'N/A')
                username = booking.get('username', 'N/A')
                price = booking.get('price', 0)

                booking_text = (
                    f"User: {username}, Location: {location}, Date: {date}, Time: {time}, "
                    f"Price: ₹{price:.2f}"
                )
                ttk.Label(scrollable_frame, text=booking_text, font=("Arial", 10)).pack(pady=2, anchor='w')

                # Smaller Cancel button next to each booking
                ttk.Button(
                    scrollable_frame,
                    text="Cancel",
                    command=lambda b=booking: self.confirm_cancel_booking(cancel_window, b)
                ).pack(pady=2, ipadx=5, ipady=2)  # Compact button size

        # Exit button at the bottom
        ttk.Button(scrollable_frame, text="Exit", command=cancel_window.destroy).pack(pady=10, ipadx=5, ipady=2)

        # Update the scroll region after all widgets are added
        cancel_window.update_idletasks()
        canvas.config(scrollregion=canvas.bbox("all"))


            
    def confirm_cancel_booking(self, index):
        if messagebox.askyesno("Confirm Cancellation", "Are you sure you want to cancel this booking?"):
            canceled_booking = self.bookings.pop(index)
            self.refund(canceled_booking['username'], canceled_booking['price'])
            self.save_data()
            messagebox.showinfo("Success", "Booking cancelled and refunded.")
         

    
    

    def add_location(self):
        loc_name = simpledialog.askstring("Add Location", "Enter new location name:")
        if loc_name:
            if loc_name in self.locations:
                messagebox.showerror("Error", "Location already exists.")
                return
            timings = simpledialog.askstring("Timings", "Enter timings for the location (e.g., 9 AM - 11 AM):")
            if not timings:
                messagebox.showerror("Error", "Timings cannot be empty.")
                return
            slots = simpledialog.askinteger("Slots", "Enter number of slots:", minvalue=1)
            if slots is not None:
                self.locations[loc_name] = {"timings": timings, "slots": slots}
                self.save_data()
                messagebox.showinfo("Success", f"Location '{loc_name}' added successfully.")
            else:
                messagebox.showerror("Error", "Invalid number of slots.")
        else:
            messagebox.showerror("Error", "Location name cannot be empty.")

    def update_slots(self):
        loc_name = simpledialog.askstring("Update Slots", "Enter location name:")
        if loc_name in self.locations:
            current_slots = self.locations[loc_name].get("slots", 0)
            new_slots = simpledialog.askinteger("Slots", f"Enter new number of slots for {loc_name} (Current: {current_slots}):", minvalue=0)
            if new_slots is not None:
                self.locations[loc_name]["slots"] = new_slots
                self.save_data()
                messagebox.showinfo("Success", f"Updated slots for {loc_name} to {new_slots}.")
            else:
                messagebox.showerror("Error", "Invalid number of slots.")
        else:
            messagebox.showerror("Error", "Location not found.")

    # User Interface
    def register_user(self):
        username = simpledialog.askstring("Register", "Enter username:")
        if username:
            if username in self.users:
                messagebox.showerror("Error", "Username already exists.")
                return
            password = simpledialog.askstring("Register", "Enter password:", show='*')
            if password:
                self.users[username] = self.hash_password(password)
                self.save_data()
                messagebox.showinfo("Success", "User registered successfully!")
            else:
                messagebox.showerror("Error", "Password cannot be empty.")
        else:
            messagebox.showerror("Error", "Username cannot be empty.")

    def user_login(self):
        username = simpledialog.askstring("User Login", "Enter username:")
        if username:
            if username not in self.users:
                messagebox.showerror("Error", "User not found.")
                return
            password = simpledialog.askstring("User Login", "Enter password:", show='*')
            if password and self.verify_password(self.users[username], password):
                self.user_menu(username)
            else:
                messagebox.showerror("Error", "Incorrect password!")
        else:
            messagebox.showerror("Error", "Username cannot be empty.")

    def user_menu(self, username):
        user_window = tk.Toplevel(self.root)
        user_window.title("User Menu")
        user_window.geometry("2560x1600")

        user_frame = ttk.Frame(user_window)
        user_frame.pack(pady=20)

        ttk.Label(user_frame, text=f"Welcome, {username}!", font=("Arial", 24, 'bold')).pack(pady=10)

        ttk.Button(user_frame, text="Book a Jump", command=lambda: self.book_jump(username)).pack(pady=5, fill='x')
        ttk.Button(user_frame, text="View Bookings", command=lambda: self.view_user_bookings(username)).pack(pady=5, fill='x')
        ttk.Button(user_frame, text="Write Review", command=lambda: self.write_review(username)).pack(pady=5, fill='x')
        ttk.Button(user_frame, text="View Reviews", command=lambda: self.view_reviews()).pack(pady=5, fill='x')
        ttk.Button(user_frame, text="Write Feedback", command=lambda: self.write_feedback(username)).pack(pady=5, fill='x')
        ttk.Button(user_frame, text="Cancel Booking", command=lambda: self.cancel_user_booking(username)).pack(pady=5, fill='x')
        ttk.Button(user_frame, text="View Feedback", command=lambda: self.view_feedback()).pack(pady=5, fill='x')
        ttk.Button(user_frame, text="Exit", command=user_window.destroy).pack(pady=10, fill='x')


    def view_user_bookings(self, username):
        user_bookings_window = tk.Toplevel(self.root)
        user_bookings_window.title("Your Bookings")
        user_bookings_window.geometry("2560x1600") 

        user_bookings_frame = ttk.Frame(user_bookings_window)
        user_bookings_frame.pack(pady=10, fill="both", expand=True)

        ttk.Label(user_bookings_frame, text="Your Bookings", font=("Arial", 20, 'bold')).pack(pady=5)

        # Filter bookings for the specific user
        user_bookings = [booking for booking in self.bookings if booking.get('username') == username]

        if not user_bookings:
            ttk.Label(user_bookings_frame, text="You have no bookings.", font=("Arial", 16)).pack()
        else:
            # Create a canvas with both horizontal and vertical scrolling
            canvas = tk.Canvas(user_bookings_frame)
            h_scrollbar = ttk.Scrollbar(user_bookings_frame, orient="horizontal", command=canvas.xview)
            v_scrollbar = ttk.Scrollbar(user_bookings_frame, orient="vertical", command=canvas.yview)

            scrollable_frame = ttk.Frame(canvas)

            # Update scrollable area
            scrollable_frame.bind(
                "<Configure>",
                lambda e: canvas.configure(
                    scrollregion=canvas.bbox("all")
                )
            )

            # Place the frame in the canvas
            canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
            canvas.configure(xscrollcommand=h_scrollbar.set, yscrollcommand=v_scrollbar.set)

            # Pack the canvas and scrollbars
            canvas.pack(side="left", fill="both", expand=True)
            h_scrollbar.pack(side="bottom", fill="x")
            v_scrollbar.pack(side="right", fill="y")

            # Display each booking
            for booking in user_bookings:
                booking_text = (
                    f"Location: {booking.get('location', 'N/A')}, "
                    f"Date: {booking.get('date', 'N/A')}, "
                    f"Time: {booking.get('time', 'N/A')}, "
                    f"Price: ₹{booking.get('price', 0):.2f}"
                )
                ttk.Label(scrollable_frame, text=booking_text, font=("Arial", 10)).pack(pady=2, anchor='w')

        # Add the Exit button at the bottom
        exit_button = ttk.Button(user_bookings_window, text="Exit", command=user_bookings_window.destroy)
        exit_button.pack(pady=10)



    def write_review(self, username):
        review = simpledialog.askstring("Write Review", "Enter your review:")
        if review:
            self.reviews.append({"username": username, "review": review})
            self.save_data()
            messagebox.showinfo("Success", "Review submitted!")
        else:
            messagebox.showerror("Error", "Review cannot be empty.")

    def view_reviews(self):
        reviews_window = tk.Toplevel(self.root)
        reviews_window.title("Reviews")
        reviews_window.geometry("2560x1600")

        reviews_frame = ttk.Frame(reviews_window)
        reviews_frame.pack(pady=10)

        ttk.Label(reviews_frame, text="User Reviews", font=("Arial", 20, 'bold')).pack(pady=5)

        if not self.reviews:
            ttk.Label(reviews_frame, text="No reviews yet.", font=("Arial", 16)).pack()
        else:
            # Adding a scrollbar for better navigation if there are many reviews
            canvas = tk.Canvas(reviews_frame)
            scrollbar = ttk.Scrollbar(reviews_frame, orient="vertical", command=canvas.yview)
            scrollable_frame = ttk.Frame(canvas)

            scrollable_frame.bind(
                "<Configure>",
                lambda e: canvas.configure(
                    scrollregion=canvas.bbox("all")
                )
            )

            canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
            canvas.configure(yscrollcommand=scrollbar.set)

            canvas.pack(side="left", fill="both", expand=True)
            scrollbar.pack(side="right", fill="y")

            for review in self.reviews:
                review_text = f"{review.get('username', 'N/A')}: {review.get('review', 'N/A')}"
                ttk.Label(scrollable_frame, text=review_text, font=("Arial", 16)).pack(pady=2, anchor='w')

    def write_feedback(self, username):
        feedback = simpledialog.askstring("Write Feedback", "Enter your feedback:")
        if feedback:
            self.feedbacks.append({"username": username, "feedback": feedback})
            self.save_data()
            messagebox.showinfo("Success", "Feedback submitted!")
        else:
            messagebox.showerror("Error", "Feedback cannot be empty.")

    def cancel_user_booking(self, username):
        cancel_user_window = tk.Toplevel(self.root)
        cancel_user_window.title("Cancel Your Bookings")
        cancel_user_window.geometry("2560x1600")  # Standard size for easy viewing

        # Main frame and canvas for scrolling content
        main_frame = ttk.Frame(cancel_user_window)
        main_frame.pack(fill="both", expand=True)

        # Canvas for scrollable content
        canvas = tk.Canvas(main_frame)
        canvas.pack(side="left", fill="both", expand=True)

        # Scrollbars for vertical and horizontal scrolling
        vertical_scroll = ttk.Scrollbar(main_frame, orient="vertical", command=canvas.yview)
        horizontal_scroll = ttk.Scrollbar(main_frame, orient="horizontal", command=canvas.xview)
        vertical_scroll.pack(side="right", fill="y")
        horizontal_scroll.pack(side="bottom", fill="x")
        canvas.configure(yscrollcommand=vertical_scroll.set, xscrollcommand=horizontal_scroll.set)

        # Frame inside canvas to hold booking information
        scrollable_frame = ttk.Frame(canvas)

        # Bind scrollable area
        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )

        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")

        # Page Title
        ttk.Label(scrollable_frame, text="Your Bookings", font=("Arial", 16, 'bold')).pack(pady=5)

        # User-specific bookings
        user_bookings = [booking for booking in self.bookings if booking.get('username') == username]

        # If no bookings, show message
        if not user_bookings:
            ttk.Label(scrollable_frame, text="You have no bookings.", font=("Arial", 12)).pack(pady=5)
        else:
            for booking in user_bookings:
                # Booking details with smaller font and compact layout
                location = booking.get('location', 'N/A')
                date = booking.get('date', 'N/A')
                
                time = booking.get('time', 'N/A')
                price = booking.get('price', 0)

                booking_text = (
                    f"Location: {location}, Date: {date}, Time: {time}, Price: ₹{price:.2f}"
                )
                ttk.Label(scrollable_frame, text=booking_text, font=("Arial", 10)).pack(pady=2, anchor='w')

                # Smaller Cancel button next to each booking
                ttk.Button(
                    scrollable_frame,
                    text="Cancel",
                    command=lambda b=booking: self.confirm_cancel_booking(cancel_user_window, b)
                                    ).pack(pady=2, ipadx=5, ipady=2)  # Compact button size

        # Exit button at the bottom
        ttk.Button(scrollable_frame, text="Exit", command=cancel_user_window.destroy).pack(pady=10, ipadx=5, ipady=2)

        # Update the scroll region after all widgets are added
        cancel_user_window.update_idletasks()
        canvas.config(scrollregion=canvas.bbox("all"))

    def confirm_cancel_booking(self, window, booking):
        if messagebox.askyesno("Confirm Cancel", "Are you sure you want to cancel this booking?"):
            self.bookings.remove(booking)
            self.save_data()  # Save updated booking data
            refund_amount = booking['price']
            booking['canceled'] = True  # Mark the booking as canceled
            self.refund(booking['username'], refund_amount)
            messagebox.showinfo("Canceled", "Booking canceled successfully.")
            window.destroy()  # Close the cancel booking window


 
    
    def view_feedback(self):
        feedback_window = tk.Toplevel(self.root)
        feedback_window.title("Feedback")
        feedback_window.geometry("2560x1600")

        feedback_frame = ttk.Frame(feedback_window)
        feedback_frame.pack(pady=10)

        ttk.Label(feedback_frame, text="User Feedback", font=("Arial", 20, 'bold')).pack(pady=5)

        if not self.feedbacks:
            ttk.Label(feedback_frame, text="No feedback yet.", font=("Arial", 16)).pack()
        else:
            # Adding a scrollbar for better navigation if there are many feedbacks
            canvas = tk.Canvas(feedback_frame)
            scrollbar = ttk.Scrollbar(feedback_frame, orient="vertical", command=canvas.yview)
            scrollable_frame = ttk.Frame(canvas)


            scrollable_frame.bind(
                "<Configure>",
                lambda e: canvas.configure(
                    scrollregion=canvas.bbox("all")
                )
            )

            canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
            canvas.configure(yscrollcommand=scrollbar.set)

            canvas.pack(side="left", fill="both", expand=True)
            scrollbar.pack(side="right", fill="y")

            for feedback in self.feedbacks:
                feedback_text = f"{feedback.get('username', 'N/A')}: {feedback.get('feedback', 'N/A')}"
                ttk.Label(scrollable_frame, text=feedback_text, font=("Arial", 16)).pack(pady=2, anchor='w')

    # Book a Jump (modified with date, time, and slot selection)
    def book_jump(self, username):
        booking_window = tk.Toplevel(self.root)
        booking_window.title("Book a Jump")
        booking_window.geometry("2560x1600")

        booking_frame = ttk.Frame(booking_window)
        booking_frame.pack(pady=10)

        ttk.Label(booking_frame, text="Book a Jump", font=("Arial", 20, 'bold')).pack(pady=5)

        # Location selection
        location_var = tk.StringVar()
        locations_menu = ttk.Combobox(booking_frame, textvariable=location_var, values=list(self.locations.keys()), state='readonly')
        locations_menu.pack(pady=10)
        locations_menu.set("Select Location")

        # Date selection using Calendar widget
        ttk.Label(booking_frame, text="Select Date", font=("Arial", 16, 'bold')).pack(pady=5)
        cal = Calendar(booking_frame, selectmode='day', year=2024, month=10, day=1)
        cal.pack(pady=10)

        # Slot selection based on the location and availability
        time_var = tk.StringVar()
        slot_menu = ttk.Combobox(booking_frame, textvariable=time_var, state='readonly')
        slot_menu.pack(pady=10)
        slot_menu.set("Select Slot")

        def update_slots(event):
            selected_location = location_var.get()
            if selected_location and selected_location != "Select Location":
                location_info = self.locations[selected_location]
                slot_menu['values'] = [location_info.get('timings', 'N/A')]  # Display the available time slots
                slot_menu.set("Select Slot")
            else:
                slot_menu.set("Select Slot")
                slot_menu['values'] = []

        locations_menu.bind("<<ComboboxSelected>>", update_slots)

        # Confirm booking with date, location, and time slot
        def confirm_booking():
            selected_location = location_var.get()
            selected_date = cal.get_date()
            selected_time = time_var.get()

            if not selected_location or selected_location == "Select Location":
                messagebox.showerror("Error", "Please select a location.")
                return
            if not selected_time or selected_time == "Select Slot":
                messagebox.showerror("Error", "Please select a time slot.")
                return

            location_info = self.locations.get(selected_location, {})
            available_slots = location_info.get('slots', 0)

            if available_slots > 0:
                # Validate that the selected date is not in the past
                from datetime import datetime
                selected_datetime = datetime.strptime(selected_date, "%m/%d/%y")
                today = datetime.today()
                if selected_datetime < today:
                    messagebox.showerror("Error", "Selected date is in the past.")
                    return

                booking_price = self.price * (1 - self.discount / 100)
                self.bookings.append({
                    "username": username,
                    "location": selected_location,
                    "date": selected_date,
                    "time": selected_time,
                    "price": booking_price
                })
                location_info['slots'] = available_slots - 1
                self.save_data()
                messagebox.showinfo("Success", f"Jump booked at {selected_location} on {selected_date} for {selected_time}. Price: ₹{booking_price:.2f}")
                booking_window.destroy()
            else:
                messagebox.showerror("Error", "No slots available for this location.")

        ttk.Button(booking_frame, text="Confirm Booking", command=confirm_booking).pack(pady=20)


    def show_safety_measures(self):
        safety_window = tk.Toplevel(self.root)
        safety_window.title("Safety Measures and Terms")
        safety_window.geometry("2560x1600")

        safety_frame = ttk.Frame(safety_window)
        safety_frame.pack(pady=20, padx=20, fill="both", expand=True)

        safety_text = (

            "Terms and Conditions for Bungee Jumping:\n\n"
            "1. Age and Weight Requirements:\n"
            "   - Participants must be 12+; minors need written consent from a parent or guardian.\n"
            "   - Weight must be between 40 kg and 110 kg for safety.\n\n"
            "2. Health and Safety Requirements:\n"
            "   - Participants must be in good physical and mental health.\n"
            "   - Not allowed: heart conditions, epilepsy, vertigo, recent surgeries, pregnancy, or other health risks.\n"
            "   - A medical questionnaire may be required before participation.\n\n"
            "3. Liability Waiver:\n"
            "   - All participants (or guardians for minors) must sign a waiver acknowledging risks.\n"
            "   - Participants must follow all safety instructions.\n\n"
            "4. Booking and Cancellation Policy:\n"
            "   - Cancellations 48+ hours before the jump are eligible for refunds.\n"
            "   - No refunds for cancellations within 48 hours.\n"
            "   - Operator cancellations (e.g., weather, safety) allow for a refund or reschedule.\n\n"
            "5. Government Jurisdiction:\n"
            "   - Bookings may change or cancel based on government regulations.\n\n"
            "6. Emergency Protocols:\n"
            "   - First-aid kits and trained staff are on-site; emergency services are nearby.\n\n"
            "7. Equipment Maintenance:\n"
            "   - All gear is regularly inspected and maintained to safety standards.\n"
            "   - Participants must wear provided safety gear as instructed.\n\n"
            "8. Staff Qualifications:\n"
            "   - Certified professionals supervise all jumps and safety protocols.\n\n"
            "9. Code of Conduct:\n"
            "   - Arrive 30 minutes early for briefing.\n"
            "   - Alcohol or drugs before the jump are prohibited; violators are disqualified without refund.\n\n"
            "10. Data Privacy:\n"
            "   - Personal data is secure and used only for bookings, per privacy laws.\n\n"
            "By participating, you agree to these terms for a safe and enjoyable experience!"


        )

        ttk.Label(safety_frame, text=safety_text, font=("Arial", 14), wraplength=1050, justify="left").pack(pady=10)

        ttk.Button(safety_frame, text="Close", command=safety_window.destroy).pack(pady=10)


        
    def refund(self, username, amount):
        messagebox.showinfo("Cashback", f"{username} has received a refund of ₹{amount:.2f}")
        # Additional cashback logic can be added here if needed.




if __name__ == "__main__":
    root = tk.Tk()
    app = BungeeJumpingManagementSystem(root)
    root.mainloop()

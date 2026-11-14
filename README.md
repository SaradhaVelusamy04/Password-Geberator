# Task 1: Secure Password Generator

**Internship Program**: Auspify Technologies - Python Developer Internship  
**Difficulty**: Easy  
**Author**: Python Developer Intern  

---

## 📌 Project Overview
The **Password Generator** is a robust, customizable security tool developed in Python. It creates high-entropy, cryptographically secure passwords tailored to user specifications, safeguarding online accounts against dictionary and brute-force attacks.

Both **Interactive Command-Line (CLI)** and **Modern Graphical User Interface (GUI)** versions are provided.

---

## 🚀 Key Features
- **Cryptographic Security**: Uses Python's standard `secrets` module (CSPRNG) rather than pseudo-random numbers.
- **Customizable Length**: Choose any password length (recommended 12–32 characters).
- **Granular Character Types**:
  - Uppercase letters (`A-Z`)
  - Lowercase letters (`a-z`)
  - Digits (`0-9`)
  - Special punctuation symbols (`!@#$%^&*...`)
- **Ambiguous Character Filter**: Exclude visually confusing characters (such as `l`, `1`, `I`, `0`, `O`).
- **Real-Time Strength Meter**: Computes password entropy (bits) and gives real-time rating (*Weak, Moderate, Strong, Very Strong*).
- **Batch Generation**: Generate multiple passwords at once.
- **Persistence**: Save generated passwords directly to a file (`passwords.txt`).
- **One-Click Clipboard Copying**: Included in the GUI edition.

---

## 🛠️ Skills Demonstrated
- Python Fundamentals & OOP
- Cryptographic randomness with `secrets` and `string` modules
- Information entropy calculation (`math.log2`)
- Input validation and exception handling
- Tkinter GUI design with ttk widgets and modern dark styling

---

## 📁 File Structure
```
Task-1-Password-Generator/
├── password_generator.py      # Interactive CLI implementation
├── gui_password_generator.py  # Modern Tkinter GUI application
└── README.md                  # Documentation and usage guide
```

---

## 💻 How to Run

### Option 1: Command-Line Interface (CLI)
```bash
python password_generator.py
```

### Option 2: Graphical User Interface (GUI)
```bash
python gui_password_generator.py
```

---

## 📸 Workflow Steps Completed
1. **Take password length as input**: Slider in GUI, validated numeric prompt in CLI.
2. **Include letters, numbers, and symbols**: Checkboxes / toggles for all categories.
3. **Generate a random password**: Securely sampled and shuffled.
4. **Display the generated password**: Centered dynamic display with strength badge.
5. **Allow users to generate multiple passwords**: Batch loop in CLI & interactive regeneration in GUI.

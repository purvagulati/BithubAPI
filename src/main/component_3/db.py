# PR Description
PR_DESCRIPTION_DATABASE = {
    1: {
        "request": {
            "repository_id": 100,
            "committed_changes": {
                "code_changes": [
                    {
                        "file_path": "src/main.py",
                        "original_code": "def add(a, b):\n    return a + b",
                        "modified_code": "def add(a, b):\n    return a + b + c",
                        "change_status": 1  # COMMITTED
                    }
                ]
            }
        },
        "response": {
            "draft_description": "Modified the add function in src/main.py to include an additional parameter 'c'."
        }
    },
    2: {  # Example 2
        "request": {
            "repository_id": 101,
            "committed_changes": {
                "code_changes": [
                    {
                        "file_path": "src/utils.py",
                        "original_code": "def multiply(a, b):\n    return a * b",
                        "modified_code": "def multiply(a, b, c=1):\n    return a * b * c",
                        "change_status": 1  # COMMITTED
                    }
                ]
            }
        },
        "response": {
            "draft_description": "Added an optional third parameter 'c' to the multiply function in src/utils.py."
        }
    },
    3: {  # Example 3
        "request": {
            "repository_id": 102,
            "committed_changes": {
                "code_changes": [
                    {
                        "file_path": "src/api_handler.py",
                        "original_code": "def handle_request(request):\n    # Process request",
                        "modified_code": "def handle_request(request):\n    # Enhanced request processing",
                        "change_status": 1  # COMMITTED
                    }
                ]
            }
        },
        "response": {
            "draft_description": "Enhanced the request handling logic in src/api_handler.py."
        }
    }
}



# Smart Autocomplete

SMART_AUTOCOMPLETE_DATABASE = {
    1: { # Suggests completing a Python addition function.
        "request": {
            "repository_content": {
                "files": [
                    {
                        "file_path": "src/main.py", 
                        "content": "def add(a, b):\n    "
                    }
                ]
            },
            "committed_changes": {
                "code_changes": [
                    {
                        "file_path": "src/main.py", 
                        "original_code": "", 
                        "modified_code": ""
                        }
                ]
            },
            "uncommitted_changes": {
                "code_changes": [
                    {
                        "file_path": "src/main.py", 
                        "original_code": "", 
                        "modified_code": ""
                    }
                ]
            },
            "recent_edits": {
                "edits": [
                    {
                        "file_path": "src/main.py", 
                        "line_number": 2, 
                        "before_edit": "", 
                        "after_edit": ""
                    }
                ]
            }
        },
        "response": {
            "completion_suggestion": "return a + b"
        }
    },
    2: { # Suggests completing a Python factorial function.
        "request": {
            "repository_content": {
                "files": [
                    {
                        "file_path": "src/math_utils.py", 
                        "content": "def factorial(n):\n    if n == "
                    }
                ]
            },
            "committed_changes": {
                "code_changes": [
                    {
                        "file_path": "src/math_utils.py", 
                        "original_code": "def add(a, b):", 
                        "modified_code": "def add(a, b, c):"
                    }
                ]
            },
            "uncommitted_changes": {
                "code_changes": [
                    {
                        "file_path": "src/math_utils.py", 
                        "original_code": "def subtract(a, b):", 
                        "modified_code": "def subtract(a, b, c):"
                    }
                ]
            },
            "recent_edits": {
                "edits": [
                    {
                        "file_path": "src/math_utils.py", 
                        "line_number": 2, 
                        "before_edit": "if n == 1", 
                        "after_edit": "if n == "
                    }
                ]
            }
        },
        "response": {
            "completion_suggestion": "0: return 1\n    else: return n * factorial(n - 1)"
        }
    },
    3: { # Provides a JavaScript function to check if a number is prime.
        "request": {
            "repository_content": {
                "files": [
                    {
                        "file_path": "src/main.js", 
                        "content": "function isPrime(num) {\n    for (let i = 2; i < num; i++)"
                    }
                ]
            },
            "committed_changes": {
                "code_changes": [
                    {
                        "file_path": "src/main.js", 
                        "original_code": "function add(a, b) {", 
                        "modified_code": "function add(a, b, c) {"
                    }
                ]
            },
            "uncommitted_changes": {
                "code_changes": [
                    {
                        "file_path": "src/main.js",
                        "original_code": "function subtract(a, b) {", 
                        "modified_code": "function subtract(a, b, c) {"
                    }
                ]
            },
            "recent_edits": {
                "edits": [
                    {
                        "file_path": "src/main.js", 
                        "line_number": 2, 
                        "before_edit": "for (let i = 2; i <= Math.sqrt(num); i++)", 
                        "after_edit": "for (let i = 2; i < num; i++)"
                    }
                ]
            }
        },
        "response": {
            "completion_suggestion": "if (num % i === 0) return false;\n    }\n    return num > 1;"
        }
    },

    4: { #Offers a SQL query to select all active users from a users table
        "request": {
            "repository_content": {
                "files": [
                    {
                        "file_path": "queries.sql", 
                        "content": "SELECT * FROM users WHERE "
                    }
                ]
            },
            "committed_changes": {
                "code_changes": [
                    {
                        "file_path": "queries.sql", 
                        "original_code": "SELECT id FROM users", 
                        "modified_code": "SELECT * FROM users"
                    }
                ]
            },
            "uncommitted_changes": {
                "code_changes": [
                    {
                        "file_path": "queries.sql", 
                        "original_code": "SELECT name FROM users", 
                        "modified_code": "SELECT name, email FROM users"
                    }
                ]
            },
            "recent_edits": {
                "edits": [
                    {
                        "file_path": "queries.sql", 
                        "line_number": 1, 
                        "before_edit": "SELECT * FROM users WHERE id = 1", 
                        "after_edit": "SELECT * FROM users WHERE "
                    }
                ]
            }
        },
        "response": {
            "completion_suggestion": "user_status = 'active'"
        }
    }
}

# Chatgpt for Code

CHATGPT_CODE_DATABASE = { 
# 1 sample response - Task to add a function to calculate sum of 2 number
    1: {
        "request": {
            "task_description": "Add a function to calculate the sum of two numbers",
            "repository_id": 100,
            "committed_changes": {
                "code_changes": [
                    {
                        "file_path": "src/math_utils.py", 
                        "original_code": "def multiply(a, b): return a * b", 
                        "modified_code": "def multiply(a, b, c=1): return a * b * c"
                    }
                ]
            },
            "uncommitted_changes": {
                "code_changes": [
                    {
                        "file_path": "src/main.py", 
                        "original_code": "print('Hello')", 
                        "modified_code": "print('Hello, world!')"
                    }
                ]
            }
        },
        "response": {
            "response": "Function 'add' added to src/math_utils.py",
            "delta": {
                "is_it_committed": False,
                "changes": [
                    {
                        "file_path": "src/math_utils.py",
                        "original_code": "",
                        "modified_code": "def add(a, b): return a + b"
                    }
                ]
            },
            "needs_clarification": False
        }
    },
    
# 2 sample response - Task to create a function that checks if a number is prime in Python.
    2: { 
        "request": {
            "task_description": "Create a Python function to check if a number is prime",
            "repository_id": 101,
            "committed_changes": {
                "is_it_committed": False,
                "code_changes": [
                    {
                        "file_path": "src/math_utils.py", 
                        "original_code": "def add(a, b): return a + b", 
                        "modified_code": "def add(a, b, c=1): return a + b * c"
                    }
                ]
            },
            "uncommitted_changes": {
                "code_changes": [
                    {
                        "file_path": "src/main.py", 
                        "original_code": "print('Starting')", 
                        "modified_code": "print('Processing')"
                    }
                ]
            }
        },
        "response": {
            "response": "Prime checking function added to src/math_utils.py",
            "delta": {
                "is_it_committed": False,
                "changes": [
                    {
                        "file_path": "src/math_utils.py",
                        "original_code": "",
                        "modified_code": "def is_prime(num):\n    if num < 2:\n        return False\n    for i in range(2, num):\n        if num % i == 0:\n            return False\n    return True"
                    }
                ]
            },
            "needs_clarification": False
        }
    },

# 3 sample response - Modify an existing JavaScript function to add error handling
    3: { 
        "request": {
            "task_description": "Add error handling to the existing 'parseData' JavaScript function",
            "repository_id": 102,
            "committed_changes": {
                "is_it_committed": False,
                "code_changes": [
                    {
                        "file_path": "src/utils.js", 
                        "original_code": "function parseData(data) { return JSON.parse(data); }", 
                        "modified_code": ""
                    }
                ]
            },
            "uncommitted_changes": {
                "code_changes": [
                    {
                        "file_path": "src/index.js", 
                        "original_code": "console.log('Ready');", 
                        "modified_code": "console.log('Initializing');"
                    }
                ]
            }
        },
        "response": {
            "response": "Error handling added to 'parseData' function in src/utils.js",
            "delta": {
                "is_it_committed": False,
                "changes": [
                    {
                        "file_path": "src/utils.js",
                        "original_code": "",
                        "modified_code": "function parseData(data) {\n    try {\n        return JSON.parse(data);\n    } catch (error) {\n        console.error('Parsing error:', error);\n    }\n}"
                    }
                ]
            },
            "needs_clarification": False
        }
    },
    
# 4 sample response - Write a SQL query for selecting users with a specific condition, 
# but the task description is unclear, requiring clarification.
  4: {
        "request": {
            "task_description": "Write a SQL query to select users",
            "repository_id": 103,
            "committed_changes": {
                "code_changes": [
                    {
                        "file_path": "queries.sql", 
                        "original_code": "SELECT * FROM users;", 
                        "modified_code": ""
                    }
                ]
            },
            "uncommitted_changes": {
                "code_changes": [
                    {
                        "file_path": "db_config.py", 
                        "original_code": "DATABASE_URL = 'localhost'", 
                        "modified_code": "DATABASE_URL = 'db.example.com'"
                    }
                ]
            }
        },
        "response": {
            "response": "Clarification needed: Please specify the criteria for selecting users.",
            "delta": {},
            "needs_clarification": True
        }
    }
}

# 4. VIRTUAL PAIR PROGRAMMING
VIRTUAL_PAIR_PROGRAMMING_DATABASE = {
    1: {
        "request": {
            "repository_id": 200,
            "existing_code": [
                {
                    "file_path": "src/app.py", 
                    "original_code": "print('Hello world')", 
                    "modified_code": "print('Hello universe')", 
                    "change_status": "UNCOMMITTED"
                }
            ],
            "stack_trace": [
                {
                    "file_name": "app.py", 
                    "line_number": 10, 
                    "method_name": "main", 
                    "code_context": "print('Hello universe')"
                }
            ],
            "issue_description": "Application crashes on startup"
        },
        "response": {
            "conversation": [
                {
                    "speaker": "user", 
                    "message": "The app crashes when I run it.", 
                    "timestamp": "2023-12-08 10:00:00"
                },
                {
                    "speaker": "AI", 
                    "message": "It looks like there's a syntax error in app.py.", 
                    "timestamp": "2023-12-08 10:01:00"
                }
            ],
            "proposed_delta": {
                "file_deltas": {
                    "is_it_committed": False,
                    "changes": [
                        {
                            "file_path": "src/app.py", 
                            "original_code": "print('Hello universe')", 
                            "modified_code": "print('Hello, universe!')", 
                            "change_status": "UNCOMMITTED"
                        }
                    ]
                }
            },
            "plain_english_description": "Fixed a syntax error in src/app.py"
        }
    },
    # Fixes a subtraction error in an addition function.
    2: {
        "request": {
            "repository_id": 201,
            "existing_code": [
                {
                    "file_path": "src/utils.py",
                    "original_code": "def add(a, b): return a + b",
                    "modified_code": "def add(a, b): return a - b",
                    "change_status": "UNCOMMITTED"
                }
            ],
            "stack_trace": [
                {
                    "file_name": "utils.py",
                    "line_number": 5,
                    "method_name": "add",
                    "code_context": "return a - b"
                }
            ],
            "issue_description": "Incorrect addition result"
        },
        "response": {
            "conversation": [
                {
                    "speaker": "user",
                    "message": "The add function is returning wrong results.",
                    "timestamp": "2023-12-08 11:00:00"
                },
                {
                    "speaker": "AI",
                    "message": "The problem seems to be in the subtraction operation in the add method.",
                    "timestamp": "2023-12-08 11:01:00"
                }
            ],
            "proposed_delta": {
                "file_deltas": {
                    "is_it_committed": False,
                    "changes": [
                        {
                            "file_path": "src/utils.py",
                            "original_code": "def add(a, b): return a - b",
                            "modified_code": "def add(a, b): return a + b",
                            "change_status": "UNCOMMITTED"
                        }
                    ]
                }
            },
            "plain_english_description": "Fixed the subtraction error in add method in src/utils.py"
        }
    },
    #  Corrects a typo in a configuration file (DEBUG variable).
    3: {
        "request": {
            "repository_id": 202,
            "existing_code": [
                {
                    "file_path": "src/config.py",
                    "original_code": "DEBUG = Flase",
                    "modified_code": "DEBUG = False",
                    "change_status": "UNCOMMITTED"
                }
            ],
            "stack_trace": [],
            "issue_description": "Syntax error in configuration file"
        },
        "response": {
            "conversation": [
                {
                    "speaker": "user",
                    "message": "There's a typo in the config file.",
                    "timestamp": "2023-12-08 12:00:00"
                },
                {
                    "speaker": "AI",
                    "message": "The issue is a misspelling in the DEBUG variable.",
                    "timestamp": "2023-12-08 12:01:00"
                }
            ],
            "proposed_delta": {
                "file_deltas": {
                    "is_it_committed": False,
                    "changes": [
                        {
                            "file_path": "src/config.py",
                            "original_code": "DEBUG = Flase",
                            "modified_code": "DEBUG = False",
                            "change_status": "UNCOMMITTED"
                        }
                    ]
                }
            },
            "plain_english_description": "Corrected typo in DEBUG variable in src/config.py"
        }
    },
    # Adds a timeout to API requests to handle potential freezing issues.
    4: {
        "request": {
            "repository_id": 203,
            "existing_code": [
                {
                    "file_path": "src/api_handler.py",
                    "original_code": "response = requests.get(url)",
                    "modified_code": "response = requests.get(url, timeout=10)",
                    "change_status": "UNCOMMITTED"
                }
            ],
            "stack_trace": [
                {
                    "file_name": "api_handler.py",
                    "line_number": 25,
                    "method_name": "fetch_data",
                    "code_context": "response = requests.get(url)"
                }
            ],
            "issue_description": "API calls timeout not handled"
        },
        "response": {
            "conversation": [
                {
                    "speaker": "user",
                    "message": "Sometimes the API calls freeze the app.",
                    "timestamp": "2023-12-08 13:00:00"
                },
                {
                    "speaker": "AI",
                    "message": "Adding a timeout to the API request should resolve this issue.",
                    "timestamp": "2023-12-08 13:01:00"
                }
            ],
            "proposed_delta": {
                "file_deltas": {
                    "is_it_committed": False,
                    "changes": [
                        {
                            "file_path": "src/api_handler.py",
                            "original_code": "response = requests.get(url)",
                            "modified_code": "response = requests.get(url, timeout=10)",
                            "change_status": "UNCOMMITTED"
                        }
                    ]
                }
            },
            "plain_english_description": "Added timeout to API request in src/api_handler.py"
        }
    }
}


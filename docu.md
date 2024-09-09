# XMP File Format Documentation

## Overview

The `.xmp` file format is designed to store and execute metadata, scripts, and configurations in a structured and readable manner. This documentation provides a detailed overview of the syntax, commands, and features available in the `.xmp` file format.

## File Structure

An `.xmp` file typically starts with the `$xmp` keyword, followed by metadata and various sections for data storage, conditional statements, loops, functions, and more.

### Example Structure

```plaintext
$xmp
Version: 1.0
Author: John Doe
CreationDate: 2024-09-09

data:
    name: "Alice"
    age: 30
    scores: [85, 90, 78]

if age > 18:
    status: "Adult"
else:
    status: "Minor"

for score in scores:
    print("Score:", score)

def greet(name):
    return f"Hello, {name}!"

greeting_message: greet(name)

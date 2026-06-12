import re

# Read the file
with open('app_enhanced.py', 'r', encoding='utf-8') as f:
    content = f.read()

# Replace the deprecated parameter with the new one
# We replace use_column_width=True with use_container_width=True
# This is better for mobile responsiveness too!
new_content = content.replace('use_column_width=True', 'use_container_width=True')

# Write the file back
with open('app_enhanced.py', 'w', encoding='utf-8') as f:
    f.write(new_content)

print("✅ Fixed deprecation warning!")
print("✅ Switched to 'use_container_width' for better mobile scaling.")
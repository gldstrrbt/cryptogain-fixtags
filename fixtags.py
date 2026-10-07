import os

def open_file(filepath):
	try:
		a = open(filepath, "r", encoding="utf8", errors="ignore")
		return a.readlines()
	except Exception as e:
		print(f"Error opening file {filepath}: {e}")
		return []

def write_file(filepath, data):
	try:
		a = open(filepath, "w", encoding="utf8", errors="ignore")
		a.write(data)
		return True
	except Exception as e:
		print(f"Error writing to file {filepath}: {e}")
		return False

def get_meta(dataset):
	dash_count = 0
	meta_array = []
	for a in dataset:
		if "---" in str(a):
			dash_count += 1
		meta_array.append(a)
		if dash_count >= 2:
			break
	return meta_array

def get_body(dataset):
	dash_count = 0
	body_array = []
	for a in dataset:
		if "---" in str(a):
			dash_count += 1
		if dash_count >= 2 and "---" not in str(a):
			body_array.append(a)
	return body_array

def change_tag_case(meta_array):
	tag_detected = False
	for b, a in enumerate(meta_array):
		if "tags:" in str(a):
			tag_detected = True
			continue
		if tag_detected and (":" in str(a) or "---" in str(a)):
			tag_detected = False
		if tag_detected and "-" in str(a) and "---" not in str(a):
			original = meta_array[b]
			meta_array[b] = meta_array[b].lower()
			if original != meta_array[b]:
				print(f"Changed tag: '{original.strip()}' to '{meta_array[b].strip()}'")
	return meta_array

def process_file(filepath):
	print(f"Processing: {filepath}")
	file_data = open_file(filepath)
	if not file_data:
		return False
	
	meta_data = get_meta(file_data)
	meta_data = change_tag_case(meta_data)
	body_data = get_body(file_data)
	
	modified_content = "".join(meta_data + body_data)
	return write_file(filepath, modified_content)

def process_directory(directory_path):
	"""
	Recursively walk through all directories and process markdown files
	"""
	processed_count = 0
	skipped_count = 0
	
	for root, dirs, files in os.walk(directory_path):
		for file in files:
			# Check if the file is a markdown file
			if file.endswith(('.md', '.markdown')):
				full_path = os.path.join(root, file)
				success = process_file(full_path)
				if success:
					processed_count += 1
				else:
					skipped_count += 1
	
	print(f"\nSummary:")
	print(f"Processed {processed_count} files successfully")
	print(f"Skipped {skipped_count} files due to errors")

def main():
	# Replace with your directory path
	directory_path = "date_structure"
	
	# Ask for confirmation
	print(f"This will recursively process all markdown files in: {directory_path}")
	confirm = input("Do you want to proceed? (y/n): ")
	
	if confirm.lower() == 'y':
		process_directory(directory_path)
	else:
		print("Operation cancelled.")

if __name__ == "__main__":
	main()
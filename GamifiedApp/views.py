import requests
from django.http import HttpResponse

def index(request):
    custom_course_id = request.POST.get("custom_course_id", "DefaultCourseID")
    custom_user_id = request.POST.get("custom_user_id", "DefaultUserID")
    custom_assignment_id = request.POST.get("custom_assignment_id", "DefaultAssignmentID")

    # Define the Canvas API endpoint for retrieving users in a course
    course_id = custom_course_id  # Replace with your actual course ID
    users_url = f"https://canvas.instructure.com/api/v1/courses/{course_id}/users"

    # Include your Canvas API token here (replace 'YOUR_API_TOKEN')
    api_token = '7~gpmiTv0LaSCQoS5vQBzBO5tfngyET0z8nmulp3uESU6YrsMCFKpJz4qW4NWeYhhC'

    # Define headers with API token
    headers = {
        'Authorization': f'Bearer {api_token}',
    }

    try:
        # Make an API request to retrieve user data
        response = requests.get(users_url, headers=headers)

        if response.status_code == 200:
            user_data = response.json()

            # Extract user information
            user_list = []
            for user in user_data:
                user_name = user.get('name', 'Unknown')
                user_id = user.get('id')
                user_list.append(user_name)

                # Check each user's assignments for the specified assignment
                assignments_url = f"https://canvas.instructure.com/api/v1/courses/{course_id}/assignments/{custom_assignment_id}/submissions/{user_id}"
                assignment_response = requests.get(assignments_url, headers=headers)
                submission_status = "WORK Not Submitted"
                if assignment_response.status_code == 200:
                    submission_data = assignment_response.json()
                    if submission_data.get('workflow_state') == 'submitted':
                        submission_status = "Work Submitted"
                user_list.append(f"Assignment Trail: {submission_status}")

            user_information = "<br><br>".join(user_list)
        else:
            user_information = "Failed to retrieve user data."
    except requests.exceptions.RequestException as e:
        user_information = "Failed to retrieve user data."

    return HttpResponse(f"Welcome user: {custom_user_id} to the course with ID: {custom_course_id}<br><br>List of Users and Their Assignments:<br>{user_information}")

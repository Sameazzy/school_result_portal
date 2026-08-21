from django.db import models
from django.contrib.auth.models import User

class ClassRoom(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()

    def __str__(self):
        return self.name

class Teacher(models.Model):
    """Represents a teacher assigned to a classroom."""

    # Link teacher to a Django user account for login.
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE
    )

    # Assign the teacher to one classroom.
    classroom = models.ForeignKey(
        ClassRoom,
        on_delete=models.CASCADE
    )

    # Display the teacher's name or username.
    def __str__(self):
        return self.user.get_full_name() or self.user.username

class Student(models.Model):
    # Connect each student to a Django user account.
    # This will be used for authentication and login.
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        null=True,
        blank=True
    )

    # Automatically generated admission number.
    admission_number = models.CharField(
        max_length=20,
        unique=True,
        blank=True
    )

    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)

    # Student's gender.
    # M = Male
    # F = Female
    gender = models.CharField(
        max_length=1,
        choices=[
            ("M", "Male"),
            ("F", "Female"),
        ],
        blank=True,
        null=True
    )

    # The class the student belongs to.
    classroom = models.ForeignKey(
        ClassRoom,
        on_delete=models.CASCADE
    )

    def save(self, *args, **kwargs):
        """
        Automatically generate an admission number
        when a new student is created.
        """

        # Only generate an admission number if one
        # has not already been assigned.
        if not self.admission_number:

            # Get the most recently created student.
            last_student = Student.objects.order_by("-id").first()

            if last_student:
                next_number = last_student.id + 1
            else:
                next_number = 1

            # Generate numbers such as:
            # STU001
            # STU002
            # STU003
            self.admission_number = f"STU{next_number:03d}"

        # Save the student normally.
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"

class Subject(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()

    def __str__(self):
        return self.name
class AcademicSession(models.Model):
    session = models.CharField(max_length=20) 

    term = models.CharField(
        max_length=20,
        choices=[
            ('First Term', 'First Term'),
            ('Second Term', 'Second Term'),
            ('Third Term', 'Third Term')
        ]
    )
    def __str__(self):
        return f"{self.session} - {self.term}"

class Score(models.Model):
    student = models.ForeignKey(
        Student, 
        on_delete=models.CASCADE
    )
    subject = models.ForeignKey(
            'Subject',
            on_delete=models.CASCADE
    )
    academic_session = models.ForeignKey(
        AcademicSession, 
        on_delete=models.CASCADE
    )
    
    ca_score = models.DecimalField(
        max_digits=5, 
        decimal_places=2
    )
    exam_score = models.DecimalField(
        max_digits=5, 
        decimal_places=2
    )

    #Calculate student's total for subject
    @property
    def total(self):
        return self.ca_score + self.exam_score

    #Convert the total to appropraite grade
    @property
    def grade(self):
        total = self.total
        if total >= 70:
            return 'A'
        elif total >= 60:
            return 'B'
        elif total >= 50:
            return 'C'
        elif total >= 45:
            return 'D'
        else:
            return 'F'

    #Provide a descriptive remark based on the grade
    @property
    def remark(self):
        remarks = {
            "A": "Excellent",
            "B": "Very Good",
            "C": "Good",
            "D": "Fair",
            "E": "Pass",
            "F": "Fail",
        }

        return remarks[self.grade]

    def __str__(self):
        return f"{self.student}"

    class Meta:
        # Prevent duplicate entry for a student for the same subject 
        # in the same academic session/term 
        constraints = [
            models.UniqueConstraint(
                fields=[
                    "student",
                    "subject",
                    "academic_session"
                ],
                name="unique_student_subject_session"
            )
        ]
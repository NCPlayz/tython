class Student:
    fullName: str

    def __init__(self, firstName: str, middleInitial: str, lastName: str):
        self.fullName = firstName + ' ' + middleInitial + ' ' + lastName


class Person:
    firstName: str
    lastName: str


def greeter(person: Person):
    return 'Hello, ' + person.firstName + ' ' + person.lastName


user = Student('Jane', 'M.', 'User')
document.body.textContent = greeter(user)


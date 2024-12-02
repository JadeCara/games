# Tic Tac Toe Game

## How to Run the Project

To run the project locally, follow these steps:

1. **Clone the repository**:
```sh
git clone <repository-url>
cd games
```


2. **Set Up Environment**:

Two Options here:

Run it locally:

```sh
make venv
source venv/bin/activate  # On Windows use `venv\Scripts\activate`
make run
```

Run it on the docker:

```sh
make build
make docker_run
```

Navigate to localhost: http://0.0.0.0:8000/

> [!TIP]
> You will need to start a new game before you can enter any coordinates.
> The Coordinates use computer numbering starting with 0. ie (0, 0) (1, 0), (2, 0) etc.

### How much time you spent building the project
I spent between 3.5 and 4 hours on this project. I was mainly focused on the game and game context as well as the api elements. I used Github Copilot to make an interface. I also saved quite a bit of time by using a python set up template to get my MakeFile, DockerFile etc in place right away.

### Any assumptions you made
I assumed the user does know how to play tic tac toe. I also assumed the x, y coordinates would make sense to the user. 

### Any trade-offs you made
Testing is really important to me. So I spent quite a bit of time on writing tests rather than making the interface pretty. 

### Any special/unique features you added
This PR also has github actions which run on push and PR.

### Anything else you want us to know about
I used Pydantic as a nice way to validate inputs. It can also be used to autogen openapi specs which I did not do this time. 

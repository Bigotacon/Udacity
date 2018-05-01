import fresh_tomatoes
import media

heart_of_a_dog = media.Movie("Heart of A Dog",
                        "A biting satire of the New Soviet man, it was created in 1925 at the height of the NEP period, when Communism appeared to be weakening in the Soviet Union.",
                        "http://tse4.mm.bing.net/th?id=OIP.M58655e4257273e88badc311f6c827e95o2&pid=15.1",
                        "https://www.youtube.com/watch?v=R-2pOQcbFx4")

battleship_potemkin = media.Movie("Battleship Pokemkin",
                     "Fed up with the extreme cruelties of their officers and their maggot-ridden meat rations, the sailors stage a violent mutiny. This, in turn, sparks an abortive citizens' revolt against the Czarist regime.",
                     "https://upload.wikimedia.org/wikipedia/commons/8/85/Vintage_Potemkin.jpg",
                     "https://www.youtube.com/watch?v=kS5kzTbNKjs")

the_intouchables = media.Movie("The Intouchables",
                             "In Paris, the aristocratic and intellectual Philippe is a quadriplegic millionaire who is interviewing candidates for the position of his carer, with his red-haired secretary Magalie.",
                             "http://ia.media-imdb.com/images/M/MV5BMTYxNDA3MDQwNl5BMl5BanBnXkFtZTcwNTU4Mzc1Nw@@._V1_SY1000_CR0,0,674,1000_AL_.jpg",
                             "https://www.youtube.com/watch?v=34WIbmXkewU")

the_lives_of_others = media.Movie("The Lives of Others",
                                  "In 1984 East Berlin, an agent of the secret police, conducting surveillance on a writer and his lover, finds himself becoming increasingly absorbed by their lives.",
                                  "http://ia.media-imdb.com/images/M/MV5BNDUzNjYwNDYyNl5BMl5BanBnXkFtZTcwNjU3ODQ0MQ@@._V1_.jpg",
                                  "https://www.youtube.com/watch?v=n3_iLOp6IhM")

phoenix = media.Movie("Phoenix",
                      "A disfigured Holocaust survivor sets out to determine if the man she loved betrayed her trust. ",
                      "http://ia.media-imdb.com/images/M/MV5BNTc3ODA4MTIxOV5BMl5BanBnXkFtZTgwNTAzOTAxNjE@._V1_.jpg",
                      "https://www.youtube.com/watch?v=zildFIFKjlc")

come_and_see = media.Movie("Come and See",
                           "After finding an old rifle, a young boy joins the Soviet resistance movement against ruthless German forces and experiences the horrors of World War II.",
                           "http://ia.media-imdb.com/images/M/MV5BMjIyMjM4NTQ2OF5BMl5BanBnXkFtZTgwOTM4MTI2MTE@._V1_.jpg",
                           "https://www.youtube.com/watch?v=6HCTIUx1Arc")


movies =[heart_of_a_dog, battleship_potemkin, the_intouchables, the_lives_of_others, phoenix, come_and_see]
fresh_tomatoes.open_movies_page(movies)

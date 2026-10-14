"""
You are given an integer mass, which represents the original mass of a planet. You are further given an integer array 
asteroids, where asteroids[i] is the mass of the ith asteroid.

You can arrange for the planet to collide with the asteroids in any arbitrary order. If the mass of the planet is greater 
than or equal to the mass of the asteroid, the asteroid is destroyed and the planet gains the mass of the asteroid. 
Otherwise, the planet is destroyed.

Return true if all asteroids can be destroyed. Otherwise, return false.
"""

def asteroids_destroyed(mass: int, asteroids: list[int]) -> bool:
    # Sort the asteroids in ascending order to maximize the chances of destroying them
    asteroids.sort()
    
    for asteroid in asteroids:
        if mass >= asteroid:
            mass += asteroid  # Planet gains the mass of the destroyed asteroid
        else:
            return False  # Planet is destroyed by the asteroid
    
    return True  # All asteroids have been destroyed
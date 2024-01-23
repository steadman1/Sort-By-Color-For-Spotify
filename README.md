# Sort Your Music by Color

## Determining One-Dimensional Color Sorting

### Requirements
- Sorting must be pleasing to the eye/aesthetic
- Must be one-dimensional

### Ideas
1. **Sort By Distance** ➡️ Take an arbitrary [a*, b*] where a is your start and b is your end point—an easy example would be white and black. From there, calculate and sort the distances between each value (r, g, b) it would take to get to the next value. [2]
2. **Sort By Relative Luminance** ➡️ Using this formula: `let luminance: Double = 0.2126 * r + 0.7152 * g + 0.0722 * b` where (r, g, b) represent given red, green, and blue values. From there, sort the luminance values. [1]
3. **Sort By Relative Brightness (HSP Color Model)** ➡️ As used in Photoshop, we can employ an RGB-to_Greyscale model to obtain brightness using the following equation: `let brightness: Double = sqrt( .299 * r_sq + .587 * g_sq + .114 * b_sq )` where (r_sq, g_sq, b_sq) represent r, g, b values that have been squared. From there, we can sort the greyscale values. [1] [3]
4. **Sort By Hue** ➡️ Using the HSL color model, we can convert each (r, g, b) value to a hue value and sort. The full equation is a bit long, but it's pretty easy to find, so you can find it in the fourth citation. [4]

### Testing
Wow, this is pretty difficult. From testing with various functions, I found the hue sorting to be by far the best, however, it doesn't take into account brightness, so holistically it looks great, but with a small list of colors, the discontinuities show a LOT more.
- ⬆️ maybe I can sort by hue and then brightness within each hue subset and make the discontinuities more artistic or something (???)
- ⬆️⬆️ Like the jumps between hues/colors would be so noticeable that it's like just separation or something.
- ⬆️ The discontinuities might not even be that noticeable either way since, at the end of the day, this is sorting album colors as a whole, not individual colors.

### Final Thoughts / Conclusion
Hue sorting was definitely the move, and I was able to accomplish exactly what I wanted to albeit with a slight hack. Here's the plain text explanation of my algorithm
1. First, I group each hue into a list of colors given by a semi-arbitrary range of max and min values for said color: e.g. reds from 0 to 0.083, yellows from 0.083 to 0.25, and so on.
2. Second, within each of the subsets of colors, I sort by greyscale (luminance would also work here)
3. Next, I use a step to grab half of each of the colors starting from 0 and 1 respectively. This essentially allowed me to create 2 lists of colors both going from light to dark.
4. Finally, I reverse the second list and combine the two lists into one making the combination go from light to dark and back to light allowing the colors, at least in a perfect world, to perfectly match between colors as they blend from as close to white as possible of one hue to as close to white as possible of another hue.

### Remarks
 - I used Swift 5 syntax for the pseudocode parts as I'm most familiar with it despite this project being in Python (sorry for that)

### Resources / Citations
- [1] https://stackoverflow.com/questions/3014402/sorting-a-list-of-colors-in-one-dimension
- [2] https://en.wikipedia.org/wiki/Dimensionality_reduction
- [3] https://alienryderflex.com/hsp.html
- [4] https://stackoverflow.com/questions/23090019/fastest-formula-to-get-hue-from-rgb
- [5] https://medium.com/towards-data-science/machine-learning-to-visually-sort-7349d3660e1

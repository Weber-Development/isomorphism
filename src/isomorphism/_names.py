"""Common first names in Swiss texts (German, French, Italian, English).

shortcut: a plain list, no spelling variants and no names of other origins; add a
Presidio backend (isomorphism.presidio) when you need more.
Words that are also common nouns or verbs (Mark, Bill, Rose, Will, Art, Hope ...) are left out.
"""

FIRST_NAMES = frozenset(
    """
    Adrian Adriano Agnes Albert Alberto Alessandro Alessia Alex Alexander Alexandra Alfred
    Alice Alina Alois Amelie Andrea Andreas Andre André Andrew Angela Angelika Anita Anja
    Anke Ann Anna Annabelle Anne Annemarie Anton Antoine Antonia Antonio Armin Arnold Arthur
    Astrid August Barbara Beat Beatrice Beatrix Beda Benedikt Benjamin Benno Bernadette
    Bernard Bernd Bernhard Berta Bettina Beatrix Brigitte Bruno Carl Carla Carlo Carmen
    Carola Carolina Caroline Catherine Cécile Charles Charlotte Chiara Christa Christian
    Christiane Christina Christine Christoph Christophe Christopher Claude Claudia Claudio
    Claus Clemens Cornelia Corinne Cristina Cyril Dagmar Damian Daniel Daniela Daniele
    Daniel David Denis Denise Dennis Diana Didier Dieter Dimitri Dino Dominik Dominique
    Doris Dorothea Edith Edgar Eduard Edwin Elena Elias Elisabeth Elise Eliane Elke Ella
    Emanuel Emil Emilie Emma Enrico Erich Erika Ernst Esther Eva Evelyn Fabian Fabio
    Fabienne Felix Fernando Filippo Finn Flavia Florence Florian Francesca Francesco Franco
    François Françoise Frank Franz Franziska Fred Frederic Friedrich Fritz Gabriel Gabriela
    Gabriele Georg George Georges Gerald Gerhard Gertrud Gianni Gilbert Gina Giorgio
    Giovanni Giulia Giuseppe Gottfried Gregor Greta Gudrun Guido Gustav Hannah Hanna Hans
    Hansjörg Hansruedi Hanspeter Harald Hedwig Heidi Heinrich Heinz Helen Helena Helene
    Helga Helmut Henri Henry Herbert Hermann Hildegard Hubert Hugo Ida Ingrid Irene Iris
    Isabel Isabelle Ivan Jacqueline Jacques Jakob Jan Jana Janine Jasmin Jean Jeanne
    Jennifer Jens Jérôme Jessica Joachim Joe Johann Johanna Johannes John Jonas Jonathan
    Josef Joseph Josephine Judith Julia Julian Julie Juliette Jürg Jürgen Karin Karl
    Katharina Katja Kaspar Kathrin Katrin Kevin Klara Klaus Konrad Kurt Lara Laura Laurent
    Lea Leandro Lena Leo Leon Leonard Leonie Lilian Lina Linda Lisa Livia Lorenz Lorenzo
    Louis Louise Luca Lucas Lucia Luciano Lucien Ludwig Luigi Luisa Luis Lukas Luzia
    Madeleine Magdalena Manfred Manuel Manuela Marc Marcel Marcello Marco Margaretha Margrit
    Maria Marianne Marie Marina Mario Marion Marius Marlene Marta Martin Martina Massimo
    Mathias Matteo Matthias Matthew Maurice Mauro Max Maximilian Maya Melanie Mélanie
    Michael Michaela Michel Michele Michelle Mirjam Miriam Monica Monika Monique Moritz
    Nadia Nadine Natalie Nathalie Nicola Nicolas Nicole Niklaus Nico Nina Noah Nora Norbert
    Olga Oliver Olivier Oskar Otto Paola Paolo Pascal Pascale Patricia Patrick Paul Paula
    Paulina Peter Petra Philipp Philippe Pia Pierre Pius Rahel Ralf Ralph Raphael Regina
    Regula Reinhard Remo René Renate Renato Reto Richard Rita Robert Roberto Roger Roland
    Rolf Romain Rosa Rosemarie Rudolf Ruedi Ruth Sabine Sabrina Salvatore Samuel
    Sandra Sandro Sara Sarah Sascha Sebastian Serge Silvan Silvia Silvio Simon Simone Sofia
    Sonja Sophie Stefan Stefania Stefano Stéphane Stephanie Stephan Steve Steven Susanne
    Sven Sylvia Sylvie Tanja Teresa Theo Theodor Therese Thierry Thomas Tim Tina Tobias Toni
    Ueli Ulrich Ulrike Ursina Ursula Urs Valentin Valentina Valérie Vanessa Verena Veronika
    Véronique Victor Viktor Vincent Vincenzo Walter Werner Wilhelm William Willi Wolfgang
    Yannick Yvonne Yves Zoe
    """.split()
)

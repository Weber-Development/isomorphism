"""Common first names in Swiss texts (German, French, Italian, English).

shortcut: a plain list, no spelling variants and no names of other origins; add a
Presidio backend (isomorphism.presidio) when you need more.
Words that are also common nouns or verbs (Mark, Bill, Rose, Will, Art, Hope ...) are left out.
"""

FIRST_NAMES = (
    frozenset(
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
    | frozenset(
        # Swiss short forms, as they appear in chats and notes.
        """
    Andi Babs Beni Chrigi Dani Fabi Fränzi Gabi Housi Kari Köbi Mäx Mike Moni Nici Röbi Sämi
    Sepp Steffi Susi Vreni Lisi Conny Tom
    """.split()
    )
    | frozenset(
        # Further names common in Switzerland: Romansh, Italian, Spanish, Portuguese, Albanian,
        # Serbo-Croatian/Bosnian, Turkish/Kurdish, Arabic, Tamil and Indian, Eritrean/Ethiopian,
        # West African, Polish. From general knowledge, not from the test texts. Names that are
        # also common words in German, French, Italian or English (Can, Luz, Gold ...) are left out.
        """
    Gion Gian Curdin Duri Flurin Flurina Ladina Mevina Seraina Andri Uorschla Mengia Chasper
    Nadja Nadine Gianluca Gianmarco Giacomo Federico Riccardo Alessio Davide Simona Federica
    Elisa Ilaria Martina Valeria Rocco Pasquale Antonella Carmela Concetta Raffaele Domenico
    Alejandro Javier Carlos Miguel Pablo Sergio Diego Jorge Alberto Lucía Ana Pilar Rocío
    Mercedes Dolores Consuelo Inmaculada Montserrat Nuria Raquel Beatriz
    João Joao José Jose Tiago Rui Nuno Duarte Gonçalo Rodrigo Vasco Bruno Ricardo Fábio Sérgio
    Inês Ines Mariana Beatriz Joana Catarina Leonor Filipa Rita Fátima Conceição Graça Elina
    Arben Besnik Valon Ardit Arbnor Ardian Bekim Blerim Driton Fatmir Florim Gëzim Ilir Kujtim
    Labinot Liridon Lulzim Mentor Naim Shkelzim Shpend Valmir Visar Xhevdet Burim Agron Artan
    Fatmire Blerta Leonora Albulena Arta Besarta Drita Donika Fjolla Lirije Mimoza Valbona
    Vjosa Shqipe Teuta Hana Ardita Edona Era Elira Elona Majlinda Nora Rina Shpresa Vlora
    Dragan Milan Goran Zoran Dejan Nenad Nikola Marko Stefan Milica Jelena Ivana Dragana Snežana
    Tomislav Ivica Damir Mirko Mario Josip Ante Luka Mateo Ana Marija Kristina Ivona Petra
    Emir Amir Edin Adnan Haris Emina Amra Lejla Selma Aida Alma Nermina
    Mehmet Mustafa Ahmet Hüseyin Hasan Ibrahim Ismail Yusuf Murat Emre Burak Kemal Cem Serkan
    Ayşe Ayse Fatma Emine Hatice Zeynep Elif Merve Esra Büşra Özlem Derya Gül Sevgi Tülay
    Muharrem Recep Yilmaz Kaan Deniz Baran Rojda Berfin Dilan Zilan Rojin Azad Rêber
    Mohammed Mohamed Muhammad Ahmed Ali Omar Youssef Karim Hamza Khaled Samir Tarek Bilal
    Fatima Aisha Amina Khadija Mariam Yasmin Leila Nour Rania Salma Samira Zainab
    Priya Arjun Kumar Suresh Ramesh Rajesh Ganesh Vijay Anand Karthik Pradeep Prakash Sanjay
    Lakshmi Kavitha Nirmala Shanthi Vasanthi Thushara Tharshini Thamilini Kajan Mathan Nirojan
    Sivakumar Thanushan Thurka Janani Abinaya Kiruthika Sutharsan Mayuran Anushan Rajan
    Yonas Yohannes Filmon Merhawi Mussie Tesfay Tesfalem Habtom Senait Selam Semhar Saba Helen
    Tsega Luwam Rahwa Feven Meron Abel Dawit Kidane Ermias Aklilu Hiwet Mebrat
    Chidi Emeka Chinedu Ngozi Ifeoma Adaeze Amara Oluwaseun Ousmane Mamadou Moussa Ibrahima
    Aminata Fatou Awa Mariama Kadiatou Seydou Lamine Abdoulaye Boubacar
    Andrzej Piotr Krzysztof Tomasz Marcin Paweł Michał Agnieszka Katarzyna Małgorzata Joanna
    Magdalena Monika Ewa Zofia Wojciech
    """.split()
    )
)

echo "TEST Toklien"
grep html public/index.html | wc -l
grep "<h1>Tolkien Fan Club</h1>" public/index.html | wc -l
grep "<li>Gandalf</li>" public/index.html | wc -l
grep "<i>didn't ruin it</i>" public/index.html | wc -l
grep "<b>I like Tolkien</b>" public/index.html | wc -l
grep "<a href" public/index.html | wc -l
grep "<li>It can be enjoyed by children and adults alike</li>" public/index.html | wc -l
grep "<code>" public/index.html | wc -l
grep '<blockquote>"I am in fact a Hobbit in all but size."' public/index.html | wc -l

echo "TEST Majesty"
grep "html" public/blog/majesty/index.html | wc -l
grep "<h1>The Unparalleled Majesty" public/blog/majesty/index.html | wc -l
grep "<b>Archmage</b>" public/blog/majesty/index.html | wc -l
grep "<code>Valar</code>" public/blog/majesty/index.html | wc -l
grep "<i>legendarium</i>" public/blog/majesty/index.html | wc -l
grep "<a href" public/blog/majesty/index.html | wc -l

echo "TEST Tom"
grep "html" public/blog/tom/index.html | wc -l
grep "<h1>Why Tom Bombadil Was a Mistake" public/blog/tom/index.html | wc -l
grep "<b>Archmage</b>" public/blog/tom/index.html | wc -l
grep "<i>An unpopular opinion, I know.</i>" public/blog/tom/index.html | wc -l

echo "TEST Glorfindel"
grep "html" public/blog/glorfindel/index.html | wc -l
grep "<h1>Why Glorfindel is More" public/blog/glorfindel/index.html | wc -l
grep "<b>Legolas</b>" public/blog/glorfindel/index.html | wc -l

echo "TEST Contact"
grep "html" public/contact/index.html | wc -l
grep "<h1>Contact the Author" public/contact/index.html | wc -l
grep "<code>555" public/contact/index.html | wc -l

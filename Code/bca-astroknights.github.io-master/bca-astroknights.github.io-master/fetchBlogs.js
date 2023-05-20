var links = [];

fetch("./bloglist.txt")
    .then(x => x.text())
    .then(data => {
        links = data.replace(/\r\n/g, "\n").split("\n");
        links = cleanLinks(links);
        links.forEach(element => appendBlog(element));
    });

function cleanLinks(links) {
    for (let i = 0; i < links.length; i++) {
        if (links[i][0] == "#") {
            delete links[i];
        }
    }
    links = [...new Set(links)];

    return links;
}

function appendBlog(blogFile) {
    if (blogFile) {
        let tag = document.createElement("a");
        let title = blogFile.replace(/^.*[\\\/]/, "").replace(/\.[^/.]+$/, "");
        let text = document.createTextNode(title);
        tag.appendChild(text);
        tag.href = blogFile;
        let element = document.getElementById("blogsContainer");
        element.appendChild(tag);
        element.appendChild(document.createElement("br"));
    }
}
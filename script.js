function addTile(crossword_object,tiles_per_row,total_width) {
    var tile = document.createElement("input");

    tile.type = "text";

    dimensions = calculateTileDimensions(total_width,tiles_per_row);
    console.log(dimensions);

    var text_dimensions = dimensions.toString();
    text_dimensions = text_dimensions.concat("px");
    tile.style.height = text_dimensions;
    tile.style.width = text_dimensions;

    tile.style.margin = "5px";
    tile.style.padding = "0px";
    tile.style.textAlign = "center";
    tile.style.fontSize = "1em";
    tile.style.borderRadius = "10%";
    tile.style.borderWidth = "1px";

    crossword_object.appendChild(tile);

    tile.addEventListener("input",checkSuccessByInput);

    return(tile);
}

function addBreak(crossword_object) {
    var curr_break = document.createElement("br");
    crossword_object.appendChild(curr_break);
    return(curr_break);
}

function colorByInput(e) {
    tile = e.srcElement;

    if (tile.correct == tile.value) {
        tile.style.backgroundColor = "lightgreen";
        return true;
    } else {
        tile.style.backgroundColor = "white";
        return false;
    }
}

function checkSuccessByInput(e) {
    colorBySuccess();
}

function logInput(e) {
    console.log(e.data);
}

function contains(list,value) {
    for (i=0; i<list.length; i++) {
        if (list[i] == value) {
            return true;
        }
    }
    return false;
}

function check_success() {
    var all_tiles = document.querySelectorAll("input");
    var success = true;
    for (i=0; i < all_tiles.length; i++) {
        var curr_tile = all_tiles[i];
        if (curr_tile.value != curr_tile.correct) {
            success = false;
        }
    }
    console.log(success);
    return(success);
}

function allTilesFilled() {
    var all_tiles = document.querySelectorAll("input");
    var filled = true;
    for (i=0; i < all_tiles.length; i++) {
        var curr_tile = all_tiles[i];
        if (curr_tile.value == "") {
            filled = false;
        }
    }
    return(filled);
}

function colorBySuccess() {
    var filled_state = allTilesFilled();
    var success_state = check_success();

    if (filled_state) {
        if (success_state) {
            var replacement_color = "lightgreen";
        } else {
            var replacement_color = "red";
        }

        var all_tiles = document.querySelectorAll("input");
        for (i=0; i < all_tiles.length; i++) {
            var curr_tile = all_tiles[i];
            curr_tile.style.backgroundColor = replacement_color;
        }
    } else {
        var all_tiles = document.querySelectorAll("input");
        for (i=0; i < all_tiles.length; i++) {
            var curr_tile = all_tiles[i];
            curr_tile.style.backgroundColor = "white";
        }
    }
}

function calculateTileDimensions(overall_side,num_tiles_per_side) {
    var total_margin = 12 * num_tiles_per_side;
    var available_space = overall_side - total_margin;
    var space_per_tile = available_space / num_tiles_per_side;
    return(space_per_tile);
}

var control_dict = {
    1:{
        1:"0",
        2:"0",
        3:"8",
        4:"2",
        5:"0",
        6:"4",
        7:"0",
        8:"0",
        9:"0"
    },
    2:{
        1:"0",
        2:"9",
        3:"0",
        4:"0",
        5:"0",
        6:"0",
        7:"0",
        8:"2",
        9:"0"
    },
    3:{
        1:"3",
        2:"0",
        3:"0",
        4:"0",
        5:"0",
        6:"0",
        7:"0",
        8:"0",
        9:"0"
    },
    4:{
        1:"0",
        2:"0",
        3:"0",
        4:"4",
        5:"0",
        6:"0",
        7:"9",
        8:"0",
        9:"0"
    },
    5:{
        1:"0",
        2:"7",
        3:"0",
        4:"0",
        5:"1",
        6:"0",
        7:"0",
        8:"5",
        9:"0"
    },
    6:{
        1:"0",
        2:"0",
        3:"0",
        4:"0",
        5:"6",
        6:"3",
        7:"2",
        8:"8",
        9:"1"
    },
    7:{
        1:"0",
        2:"0",
        3:"3",
        4:"0",
        5:"0",
        6:"6",
        7:"1",
        8:"0",
        9:"2"
    },
    8:{
        1:"0",
        2:"8",
        3:"0",
        4:"0",
        5:"4",
        6:"0",
        7:"0",
        8:"6",
        9:"0"
    },
    9:{
        1:"2",
        2:"0",
        3:"0",
        4:"9",
        5:"0",
        6:"1",
        7:"0",
        8:"0",
        9:"0"
    }
}

var tiles_to_reveal = {
    1:[3,4,6],
    2:[2,8],
    3:[1],
    4:[4,7],
    5:[2,5,8],
    6:[5,6,7,8,9],
    7:[3,6,7,9],
    8:[2,5,8],
    9:[1,4,6]
}

var grid_size = 9;
var container_width = 500;

var css_width = container_width.toString();
css_width = css_width.concat("px");

var crossword = document.getElementById("crossword");

crossword.style.width = css_width;
crossword.style.height = css_width;

for (let i=0; i < grid_size; i++) {
    var row_num = i + 1;
    var curr_row = control_dict[row_num];

    var reveal_list = tiles_to_reveal[row_num];

    for (let j=0; j < grid_size; j++) {
        var curr_tile = addTile(crossword,9,container_width);

        var column_num = j + 1;

        curr_tile.correct = curr_row[column_num];

        if (contains(reveal_list,column_num)) {
            curr_tile.value = curr_tile.correct;
        }
    }
    addBreak(crossword);
}

allTilesFilled();


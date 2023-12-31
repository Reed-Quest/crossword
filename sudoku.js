function addTile(puzzle_object,tiles_per_row) {
    var tile = document.createElement("input");

    tile.type = "text";

    var total_width = puzzle_object.parentElement.clientWidth;
    total_width = parseFloat(total_width);

    dimensions = calculateTileDimensions(total_width,tiles_per_row);

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

    puzzle_object.appendChild(tile);

    tile.addEventListener("input",checkSuccessByInput);

    return(tile);
}

function addBreak(puzzle_object) {
    var curr_break = document.createElement("br");
    puzzle_object.appendChild(curr_break);
    return(curr_break);
}

function addLine(puzzle_object) {
    var curr_break = document.createElement("hr");
    puzzle_object.appendChild(curr_break);
    curr_break.className = "sudoku-horizontal-break";
    return(curr_break);
}

function addVertical(puzzle_object,height) {
    var curr_break = document.createElement("input");
    puzzle_object.appendChild(curr_break);
    curr_break.className = "vl";
    curr_break.style.height = valueToCSSPixels(height);
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
    var total_margin = 12 * num_tiles_per_side + 10;
    var available_space = overall_side - total_margin;
    var space_per_tile = available_space / num_tiles_per_side;
    return(space_per_tile);
}

function valueToCSSPixels(numeric) {
    var new_value = numeric.toString();
    new_value = new_value.concat("px");
    return(new_value);
}

var grid_size = 9;

var puzzle = document.getElementById("puzzle");

puzzle.style.clientHeight = puzzle.style.clientWidth;

var tile_dimension = calculateTileDimensions(puzzle.clientWidth,grid_size);
var vertical_height = tile_dimension * 1.6;

for (let i=0; i < grid_size; i++) {
    var row_num = i + 1;
    var curr_row = control_dict[row_num];

    var reveal_list = tiles_to_reveal[row_num];

    for (let j=0; j < grid_size; j++) {
        var curr_tile = addTile(puzzle,grid_size);

        var column_num = j + 1;

        curr_tile.correct = curr_row[column_num];

        if (contains(reveal_list,column_num)) {
            curr_tile.value = curr_tile.correct;
        }

        if (j == 2 || j == 5) {
            addVertical(puzzle,vertical_height);
        }
    }

    if (i == 2 || i == 5) {
        addLine(puzzle);
    } else {
        addBreak(puzzle);
    }
}

var explainer_text = document.getElementById("explainer-text");

explainer_text.textContent = control_text;

if (screen.width > 800) {
    explainer_text.style.position = "relative";

    var top_offset = puzzle.clientHeight;
    top_offset = top_offset/2 - explainer_text.clientHeight;
    top_offset = valueToCSSPixels(top_offset);

    explainer_text.style.top = top_offset;
}














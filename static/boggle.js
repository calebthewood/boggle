"use strict";

const $playedWords = $("#words");
const $form = $("#newWordForm");
const $wordInput = $("#wordInput");
const $message = $(".msg");
const $table = $("table");

let gameId;


/** Start */

async function start() {
  let response = await axios.post("/api/new-game");
  gameId = response.data.gameId;
  let board = response.data.board;

  //board.length = rows
  //board[0].length = columns
    //loop over board
      //content: the letter, attribute for x-y location,



  displayBoard(board);
}

/** Display board */

function displayBoard(board) {
  // $table.empty();
  //board will nested array
  // loop over board and create the DOM tr/td structure

}

/**
 * Checks word if word is valid. Returns Confirmation Message from API.
 */
async function checkWord() {
  const response = await axios.post("/api/score-word");
  const responseMsg = response.data.result;

}


start();
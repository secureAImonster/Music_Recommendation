/*
 * ラッパーのNode.jsからPythonを呼び出して実行するプログラム
 */

var exec = require('./analysis/call_pyfile');
 
/* 学習器への入力情報  
 * input_data = ["day","time","temp","weather","freq","fb", "user_id"];
 *  input 1 : day (mm/dd/yyyy)
 *  input 2 : time
 *  input 3 : temperature 
 *  input 4 : weather 
 *  input 5 : frequency
 *  input 6 : feedback 
 *  input 7 : user_id
 */

var result_recommendation = function(input_data, callback){
  exec.recommendation(input_data, function(result){
    callback(result);
  });
};


module.exports = {
  result_recommendation: result_recommendation
};

/*
 * Pythonを呼び出すNode.jsのモジュール
 */

var exec = require('child_process').exec;
 

var recommendation = function(inputs, callback) {

    /*pythonファイル実行時のPATHに注意！！*/
    var path = 'ML/analysis/';
    var exec_file = 'Recommendation.py';
    var exec_command = 'python'+' '+path+exec_file+' '+inputs[0]+' '+inputs[1]+' '+inputs[2]+' '+inputs[3]+' '+inputs[4]+' '+inputs[5]+' '+inputs[6];
    //console.log(exec_command);

    var child = exec(exec_command, function (error, stdout, stderr) {
      console.log('stdout: ' + stdout);
      console.log('stderr: ' + stderr);
      if (error !== null) {
        console.log('exec error: ' + error);
      }
      var result = stdout;
      callback(result);
    });
  };
   
var startLearning = function(input, callback) {

    /*pythonファイル実行時のPATHに注意！！*/
    var path = 'ML/analysis/';
    var exec_file = 'NeuralNetwork.py';
    var exec_command = 'python'+' '+path+exec_file+' '+ input;

    var child = exec(exec_command, function (error, stdout, stderr) {
      console.log('stdout: ' + stdout);
      console.log('stderr: ' + stderr);
      if (error !== null) {
        console.log('exec error: ' + error);
      }
      var result = stdout;
      callback(result);
    });
  };
 

  module.exports = {
    recommendation: recommendation,
    startLearning: startLearning
  };

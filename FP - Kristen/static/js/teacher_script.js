var app = angular.module('MathPartyTeacher', []);

app.config(['$interpolateProvider', function($interpolateProvider) {
  $interpolateProvider.startSymbol('{a');
  $interpolateProvider.endSymbol('a}');
}]);

app.controller("studentsGrid", ['$scope', '$http', '$interval', function($scope, $http, $interval) {
    $scope.hover = false;
    var refreshRate = 5000;
    
    var studentA = {
        name: "John Doe",
        accuracy: 0.4
    };
    var studentB = {
        name: "test2",
        accuracy: 0.6
    };
    var studentC = {
        name: "test3",
        accuracy: 0.95
    };
    var studentD = {
        name: "test4",
        accuracy: 0 
    };
    var studentE = {
        name: "test5",
        accuracy: 0.95
    };

    var students_array = [studentA, studentB, studentC, studentD, studentE];
    

    var students_array = []

    $scope.students = students_array;
    
/*
    $interval(function() {
        studentA.accuracy += 0.1;
        students_array = [studentA, studentB, studentC, studentD, studentE];
        $scope.students = students_array;
    }, 5000);
*/
    $scope.set_style = function(student) {
        student.accuracy = student.num_correct / student.num_attempted;
        console.log(student.accuracy);
        if (student.accuracy <= 0.50) {
            return {backgroundColor : "red", height: 100 + '%', overflow: "hidden", textAlign: "center"}
        }
        else if (student.accuracy <= 0.75) {
            return {backgroundColor : "yellow", height: 100 + '%', overflow: "hidden", textAlign: "center"}
        }
        else {
            return {backgroundColor : "green", height: 100 + '%', overflow: "hidden", textAlign: "center"}
        }
    }
    
   /* var ajaxCall = $interval(function() {
        $http.get("/api/api_class").then( function(response) {
            console.log(response);
            $scope.students = response.data.students;
        });
    }, refreshRate);*/
    
}]);
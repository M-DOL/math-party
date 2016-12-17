var app = angular.module('MathPartyTeacher', []);

app.config(['$interpolateProvider', function($interpolateProvider) {
  $interpolateProvider.startSymbol('{a');
  $interpolateProvider.endSymbol('a}');
}]);

app.controller("studentsGrid", ['$scope', '$http', '$interval', function($scope, $http, $interval) {
    var refreshRate = 5000;
    var minBadge = 0;
    
    /*var studentA = {
        name: "John Doe",
        accuracy: 0.4
    };
    var studentB = {
        name: "test2",
        accuracy: 0.6
    };
    var s   tudentC = {
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
    $scope.students = students_array;
    $interval(function() {
        studentA.accuracy += 0.1;
        students_array = [studentA, studentB, studentC, studentD, studentE];
        $scope.students = students_array;
    }, 5000);*/
    
    $scope.set_style = function(student) {
        var more_advanced = false;
        var accuracy = student.num_correct / student.num_attempted;
        console.log(student.name, accuracy)

        if (min_badge == 0) {
            if (student.badge_1) {
                more_advanced = true;
            }
        }
        else if (min_badge == 1) {
            if (student.badge_2) {
                more_advanced = true;
            }
        }
        else {
            if (student.badge_3) {
                more_advanced = true;
            }
        }
        
        if (accuracy <= 0.50 && !more_advanced) {
            return {backgroundColor : "red", height: 100 + '%', overflow: "hidden", textAlign: "center"}
        }
        else if (accuracy <= 0.75) {
            return {backgroundColor : "yellow", height: 100 + '%', overflow: "hidden", textAlign: "center"}
        }
        else {
            return {backgroundColor : "green", height: 100 + '%', overflow: "hidden", textAlign: "center"}
        }
    }
    
    var ajaxCall = $interval(function() {
        $http.get('../api/api_class').then( function(response) {
            console.log(response);
            $scope.students = response.data.students;
            for (student in response.data.students) {
                if (!student.badge_1 && !student.badge_2 && !student.badge_3) {
                    min_badge = 0;
                }
                else if (!student.badge_3 && !student.badge_2 && min_badge > 1) {
                    min_badge = 1;
                }
                else if (!student.badge_3 && min_badge > 2) {
                    min_badge = 2;
                }
            }
        });
    }, refreshRate);
    
}]);
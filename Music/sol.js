var K = 2;
var array = [1, 5, 3, 4, 2];

function findDifference(k, x) {
  var hash = x.reduce((prev, next) => {
       prev[next] = true;
      return prev;
   },{})

  var result = x.reduce((prev, next) => {
    return (hash[next+k]) ? prev + 1 : prev;
  }, 0)
  return result;
}

console.log(findDifference(K, array));

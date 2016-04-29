var Source = {
  filling: function(array){
    for(var i=0;i<array.length;i++)
      array[i]=Math.random(2,20);
  },
  output: function(array){
    for(var i=0;i<array.length;i++)
      console.log(array[i]+" ");
  },
  bubble_sort: function(array){
    for(var i=0;i<array.length;i++)
      for(var j=1;j<array.length;j++)
        if(array[j]<array[j-1]){
          var temp = array[j];
          array[j]=array[j-1];
          array[j-1]=temp;
        }
  },
  quick_sort: function(array,first,last)
}

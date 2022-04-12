import java.util.ArrayList;

public class CustomSort implements SortingInterface{
    private ArrayList<Double> values = new ArrayList<Double>();

    @Override
    public void setValues(ArrayList<Double> values) {
        boolean valid = true;
        if (values != null) {
            for (Double value : values) {
                if (value == null) {
                    valid = false;
                }
            }
        }
        if (valid) {
            this.values = values;
            sort();
        }
    }

    @Override
    public ArrayList<Integer> getGaps() {
        ArrayList<Integer> gaps = new ArrayList<Integer>();
        ArrayList<Integer> temp = new ArrayList<Integer>();
        int n = this.values.size();
        int gap = 1;
        int i = 2;
        while (gap < n) {
            temp.add(gap);
            gap = (1 << i) - 1;
            i++;
        }
        for (int j=(temp.size()-1);j>=0;j--) {
            gaps.add(temp.get(j));
        }
        return gaps;
    }

    @Override
    public void add(Double value) {
        if (value != null) {
            this.values.add(value);
            sort();
        }
    }

    @Override
    public void remove(int index) {
        try {
            this.values.remove(index);
        } catch (IndexOutOfBoundsException e) {
            e.printStackTrace();
        }
    }

    @Override
    public void sort() {
        int n = this.values.size();
        ArrayList<Integer> gaps = getGaps();
        for(int gap : gaps) {
            for(int i=gap;i<=(n-1);i++) {
                Double temp = this.values.get(i);
                int j = 0;
                for(j=i;j>=gap;j-=gap) {
                    if(this.values.get(j-gap)<=temp) {
                       break;
                    }
                    this.values.set(j, this.values.get(j-gap));
                }
                this.values.set(j, temp);
            }
        }
    }

    public static void main(String[] args) {
        System.out.println("Start");

        CustomSort sort = new CustomSort();
        ArrayList<Double> values = new ArrayList<Double>();
        sort.remove(2);
        sort.sort();
        values.add(0.1);
        values.add(0.5);
        values.add(0.0);
        values.add(0.2);
        values.add(0.6);
        values.add(-0.3);
        sort.setValues(values);

        System.out.println("Done");
    }
    
}

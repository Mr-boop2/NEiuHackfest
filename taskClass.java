import java.util.LinkedList;

public class TaskClass {

    private String taskName; 
    private int taskPrio; 
    private int timeEst; 
    private int nextTask; 
    private LinkedList<TaskClass> taskList; 

    public TaskClass(String taskName){
        this.taskName = taskName; 
        taskPrio = 0; 
        timeEst = 0; 
        nextTask = 0; 
        taskList = new LinkedList<>(); 
    }

    public void addTask(TaskClass taskName){
        taskList.add(taskName); 
    }


}

import numpy as np
import csv
import math
import time


def string_to_float_data(data_array):
    for i in range(len(data_array)):
    	data_array[i]=float(data_array[i])


def string_to_int_data(data_array):
    for i in range(len(data_array)):
        data_array[i]=int(data_array[i])


def index_of_movie_id(movies_id_array,movie_id):
	for i in range(len(movies_id_array)):
		if movies_id_array[i]==movie_id:
			index=i
			return index

def calculate_mean_of_an_array(array,index_of_rating_for_prediction):
    temp_array=[]
    if index_of_rating_for_prediction==-1:
      for i in range(len(array)) :
          if array[i]!=1:
             temp_array.append(array[i])
      mean=np.mean(array)
    else:
        for i in range(len(array)) :
          if array[i]!=1 and i!=j:
             temp_array.append(array[i])
        mean=np.mean(array)
    return mean 

def calculate_variance(array,mean_of_array):
    variance=0
    for i in range(len(array)):
        variance+=pow((array[i] - mean_of_array),2)
    variance=variance/len(array)
    return variance



def find_n_most_similar_movies_and_predictions_of_4_functions(n,i,j,movies_ratings,training_set,test_set,movies_ids_sorted,predictions_of_4_functions,real_ratings):

    mean_of_test_movie=calculate_mean_of_an_array(test_set[i],j)

    pearson_similarities_array=[]
    neighbours_ratings_from_same_user=[]
    common_movies_ratings=[]
    common_users_of_movies=[]
    n_variance_of_movies=[]

    for k in range(len(training_set)):
        movie_id_to_compare=movies_ids_sorted[k]
        #print("MoviedID to compare: ",movie_id_to_compare)
        if k!=len(training_set)+i :
           #Εντοπισμός των ταινιών που έχουν βαθμολογηθεί απο τον ίδιο χρήστη(μπορεί αργότερα να μην είναι χρήσιμες διότι να μην έχουν άλλες κοινές βαθμολογίες απο κοινούς χρήστες,υπάρχει σχετικό σχόλιο παρακάτω)
          if movies_ratings[k][j]!=-1:
            mean_of_training_movie=calculate_mean_of_an_array(training_set[k],-1)
            common_indices=find_common_user_ratings_between_movies(training_set[k],test_set[i],j)
        

            #Έχει μόνο νόημα να συνεχίσουμε αν οι ταινίες μεταξύ τους έχουν κοινές βαθμολογίες απο χρήστες, μπορεί να υπάρχουν συγκεκγριμένες βαθμολογίες απο συγεκριμένες χρήστες σε συγκεκριμένες ταινίες
            #για τις οποίες  δεν υπάρχουν κοντινοί γείτονες λόγω του συνολικού μεγάλου αριθμού των ταινιών και δεν μπορεί να γίνει πρόβλεψη
            
            if len(common_indices)!=0 :


              neighbours_ratings_from_same_user.append(training_set[k][j])
              common_movies_ratings.append(training_set[k])
              common_users_of_movies.append(len(common_indices))

              #print("MovieId for prediction:", movie_id_for_prediction,"UserID:",j+1,"MovieId comppared to:",movie_id_to_compare )
              temp_training_movie_common_ratings=[movies_ratings[k][l] for l in common_indices]
              temp_test_movie_common_ratings=[test_set[i][l] for l in common_indices] 
              temp_similarity=pearson_similarity(temp_training_movie_common_ratings,temp_test_movie_common_ratings,mean_of_training_movie,mean_of_test_movie) 
              pearson_similarities_array.append(temp_similarity)

    if len(pearson_similarities_array)!=0 and len(neighbours_ratings_from_same_user)!=0:

        n_neighbours_temp_indices=np.argsort(pearson_similarities_array)[-n:] 
        #Βοηθητικά arrays για την είσοδο στις 4 συναρτήσεις
        n_neighbours_similarities=[pearson_similarities_array[l] for l in n_neighbours_temp_indices]
        n_neighbours_ratings_from_same_user=[neighbours_ratings_from_same_user[l] for l in n_neighbours_temp_indices]
        n_movies_means=[calculate_mean_of_an_array(common_movies_ratings[l],-1) for l in n_neighbours_temp_indices]
        n_common_users_of_movies=[common_users_of_movies[l] for l in n_neighbours_temp_indices ]
        n_movies_ratings=[common_movies_ratings[l] for l in n_neighbours_temp_indices]
        n_variance_of_movies=[calculate_variance(n_movies_ratings[l],n_movies_means[l]) for l in range(len(n_movies_ratings))]
        
        #Οι προβλέψεις για κάθε μια απο τις ζητούμενες συναρτήσεις
        real_ratings.append(test_set[i][j])
        prediction1=round(prediction_function_1(n_neighbours_similarities,n_neighbours_ratings_from_same_user),2)
        prediction2=round(prediction_function_2(n_neighbours_similarities,n_neighbours_ratings_from_same_user,n_movies_means),2)
        prediction3=round(prediction_function_3(n_neighbours_similarities,n_neighbours_ratings_from_same_user,n_common_users_of_movies),2)
        prediction4=round(prediction_function_4(n_neighbours_similarities,n_neighbours_ratings_from_same_user,n_variance_of_movies),2)
        
       #Προσθήκη των παραπάνω προβλέψεων στα κατάλληλα arrays
        predictions_of_4_functions[0].append(prediction1)
        predictions_of_4_functions[1].append(prediction2)
        predictions_of_4_functions[2].append(prediction3)
        predictions_of_4_functions[3].append(prediction4)
        
           
    return None


def find_common_user_ratings_between_movies(movie_ratings1,movie_ratings2,user_index):
    common_indices=[]
    for j in range(len(movie_ratings1)):
        if j!=user_index and movie_ratings1[j]!=-1 and movie_ratings2[j]!=-1 :
            #print(movie_ratings1[j],movie_ratings2[j])
            common_indices.append(j)
    return common_indices


def pearson_similarity(array1,array2,mean_of_array1,mean_of_array2) :
    numerator=0
    denominator=0
    if len(array1)==len(array2):
        for i in range(len(array1)):
            numerator+=(array1[i] - mean_of_array1)*(array2[i] - mean_of_array2)
            denominator+=pow(array1[i] - mean_of_array1,2)*pow(array2[i] - mean_of_array2,2)
        denominator=math.sqrt(denominator)
        pearson_similarity=numerator/denominator
        return pearson_similarity
    else:
        print("Not the same size")

def prediction_function_1(n_similarities,n_ratings):
    similarities_sum=0
    weights=[]
    prediction=0
    for i in range(len(n_similarities)):
        similarities_sum+=n_similarities[i]
    for i in range(len(n_similarities)):
        weights.append(n_similarities[i]/similarities_sum)
    for i in range(len(n_similarities)):
        prediction+=weights[i]*n_ratings[i]
    return prediction

def prediction_function_2(n_similarities,n_ratings,means_of_n_neighbours):
    prediction=0
    numerator=0
    denominator=0
    for i in range(len(n_similarities)):
        numerator+=n_similarities[i]*(n_ratings[i]- means_of_n_neighbours[i])
        denominator+=n_similarities[i]
    prediction=numerator/denominator
    return prediction

def prediction_function_3(n_similarities,n_ratings,common_users_with_the_movie_for_prediction):
    common_users_sum=0
    weights=[]
    prediction=0
    for i in range(len(common_users_with_the_movie_for_prediction)):
        common_users_sum+=common_users_with_the_movie_for_prediction[i]
    for i in range(len(n_similarities)):
        weights.append(common_users_with_the_movie_for_prediction[i]/ common_users_sum)
    for i in range(len(n_similarities)):
        prediction+=weights[i]*n_ratings[i]
    return prediction

def prediction_function_4(n_similarities,n_ratings,n_variance_of_movies):
    variances_sum=0
    weights=[]
    prediction=0
    for i in range(len(n_variance_of_movies)):
        variances_sum+=n_variance_of_movies[i]
    for i in range(len(n_similarities)):
        weights.append(n_variance_of_movies[i]/variances_sum)
    for i in range(len(n_similarities)):
        prediction+=weights[i]*n_ratings[i]
    return prediction


def calculate_confusion_matrixes(predictions_of_4_functions,real_ratings,confusion_matrixes_of_4_functions):
    for i in range(len(predictions_of_4_functions)):
        for j in range(len(predictions_of_4_functions[0])):
         if predictions_of_4_functions[i][j]>=3 and real_ratings[j]>=3:
             #true positive
             confusion_matrixes_of_4_functions[i][0]+=1
         elif predictions_of_4_functions[i][j]<3 and real_ratings[j]<3:
             #true negative
             confusion_matrixes_of_4_functions[i][1]+=1
         elif predictions_of_4_functions[i][j]>=3 and real_ratings[j]<3:
             #false positive
             confusion_matrixes_of_4_functions[i][2]+=1
         elif predictions_of_4_functions[i][j]<3 and real_ratings[j]>=3:
             #false negative
             confusion_matrixes_of_4_functions[i][3]+=1
    return None


def calculate_metrics(confusion_matrixes_of_4_functions,metrics_array_of_4_functions,predictions_of_4_functions,real_ratings):
    for i in range(len(confusion_matrixes_of_4_functions)):
        for j in range(len(real_ratings)):
            #Calulate MAE
            metrics_array_of_4_functions[i][0]+=abs(predictions_of_4_functions[i][j] - real_ratings[j])/len(real_ratings)

        tp=confusion_matrixes_of_4_functions[i][0]
        tn=confusion_matrixes_of_4_functions[i][1]
        fp=confusion_matrixes_of_4_functions[i][2]
        fn=confusion_matrixes_of_4_functions[i][3]

        metrics_array_of_4_functions[i][0]=round(metrics_array_of_4_functions[i][0],2)
        #Calculate Precicion
        metrics_array_of_4_functions[i][1]=round(tp/(tp+fp),4)
        #Calculate Recall
        metrics_array_of_4_functions[i][2]=round(tp/(tp+fn),4)

    return None



start_time=time.time()
#Αρχικοποίηση array λιστών users_id και movies_ids_sorted
users_id=[]
movies_ids_sorted=[]

#Διάβασμα του αρχείου και άντληση των headers,δεδομένων των attributes και δεδομένων των class label
filename="ratings25000.csv"
with open(filename, 'r') as file:
    csvreader = csv.reader(file)
    headers = next(csvreader)
    for row in csvreader:
        try:
            if row[0] != None :
              movies_ids_sorted.append(row[1])
              users_id.append(row[0])
              
              
        except IndexError as e:
            print("")



string_to_int_data(movies_ids_sorted)
string_to_float_data(users_id)

#Η λίστα users_id αφού γίνει sort και αφαιρεθούν τα διπλότυπα δεδομένα περιέχει τους 610 χρήστες σε αύξουσα σειρά
users_id=list(set(users_id))
users_id.sort()
users_count=len(users_id)

#Η λίστα movies_ids_sorted αφού γίνει sort και αφαιρεθούν τα διπλότυπα δεδομένα περιέχει τις 9724 ξεχωριστές ταινίες τις οποίες βαθμολόγησαν οι χρήστες σε αύξουσα σειρά
movies_ids_sorted=list(set(movies_ids_sorted))
movies_ids_sorted.sort()

#Η λίστα users_ratings_for_all_movies περιέχει τις βαθμολογίες του κάθε χρήστη για κάθε μία απο τις ταινίες
#Δηδαδή μέσα στην users_ratings_for_all_movies βρίσκονται 610 λίστες που περιέχουν 9724 τιμές η καθεμία, ενώ η τιμή -1 συμβολίζει πως ο χρήστης δεν έχει βαθμολογίσει την αντίστοιχη ταινία
users_ratings_for_all_movies=[]

for i in range(users_count):
	#Η λίστα αρχικοποιείτα με τιμές -1 και έπειτα όποιες ταινίες έχει βαθμολογήσει ο χρήστης θα παίρνουν τις πραγματικές τιμές
	users_ratings_for_all_movies.append([-1 for x in range(len(movies_ids_sorted))])
	

with open(filename, 'r') as file:
    csvreader = csv.reader(file)
    headers = next(csvreader)
    total_classes=len(headers)
    for row in csvreader:
        try:
            if row[0] != None :
              index_of_current_user=int(row[0])-1
            
              movie_id_index=index_of_movie_id(movies_ids_sorted,int(row[1]))

              users_ratings_for_all_movies[index_of_current_user][movie_id_index]=float(row[2])
              
        except IndexError as e:
            print("123")

#Η λίστα movies_ratings_from_users μοιάζει με την users_ratings_for_all_movies αλλά αντί για τους χρήστες τα arrays αντιστοιχούν στις ταινίες
#Πλεον υπάροχυν 9724 λίστες που περιέχουν 610 (ενώ το αντίθετο ισχύει στην users_ratings_for_all_movies) 
movies_ratings_from_users=[]
for i in range(len(movies_ids_sorted)):
	movies_ratings_from_users.append([-1 for x in range(users_count)])


for i in range(len(movies_ids_sorted)):
	for j in range(users_count):
		movies_ratings_from_users[i][j]=users_ratings_for_all_movies[j][i]


#Έπειτα απο δομικές για να μοιραστούν οι βαθμολογίες σε 80% και 20% πρέπει να πάρουμε απο την λίστα movies_ratings_from_users το αρχικό 60% για το training set και το 40% για το test set
#Αυτό γίνεται επείδη κάποιες ταινίες τις έχουν βαθμολογήσει περισσότεροι χρήστες(αυτές στην αρχή της λίστας) και κάποιες λιγότεροι, έτσι χωρίζοντας τις ταινίες στο 60% και 40% παίρνουμε αντίχτοιχα το 80% και 20% των βαθμολογιών
precent_80_index_for_training_set=math.floor(0.8*len(movies_ratings_from_users))
training_set=movies_ratings_from_users[0:precent_80_index_for_training_set]
test_set=movies_ratings_from_users[precent_80_index_for_training_set:len(movies_ratings_from_users)]

print("Training_set total movies: ",len(training_set))
print("Test_set total movies: ",len(test_set))


test_ratings=0
for i in range(len(test_set)):
    for j in range(len(test_set[0])):
        if test_set[i][j]!=-1:
            test_ratings+=1

print("Test ratings : ", test_ratings)



training_ratings=0
for i in range(len(training_set)):
    for j in range(len(training_set[0])):
        if training_set[i][j]!=-1:
            training_ratings+=1

print("Training ratings  : ", training_ratings)
#--------------------------------------------------------------------------------------------------


#Confusion matrix=[tp,tn,fp,fn] για κάθε συνάρτηση πρόβλεψης
confusion_matrixes_of_4_functions=[[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0]]
#Metrics array=[MAE,Precision,Recall] για κάθε συνάρτηση πρόβλεψης
metrics_array_of_4_functions=[[0,0,0],[0,0,0],[0,0,0],[0,0,0]]

predictions_of_4_functions=[[],[],[],[]]
real_ratings=[]
n_5_for_experiment=[1,2,3,5,10]
quit=0
for n in n_5_for_experiment: 
 for i in range(len(test_set)):
     for j in range(len(test_set[0])):
        if test_set[i][j]!=-1:
            find_n_most_similar_movies_and_predictions_of_4_functions(n,i,j,movies_ratings_from_users,training_set,test_set,movies_ids_sorted,predictions_of_4_functions,real_ratings)
            quit+=1
           
        #if quit==100: 
             #break


calculate_confusion_matrixes(predictions_of_4_functions,real_ratings,confusion_matrixes_of_4_functions)
calculate_metrics(confusion_matrixes_of_4_functions,metrics_array_of_4_functions,predictions_of_4_functions,real_ratings)

for i in range(len(confusion_matrixes_of_4_functions)):
    for j in range(len(confusion_matrixes_of_4_functions[0])):
        confusion_matrixes_of_4_functions[i][j]=confusion_matrixes_of_4_functions[i][j]/5
print("\nΜέσος όρος confusion matrix για τα δοκιμασμένα n=[1,2,3,5,10] της Συνάρτησης 1: ",confusion_matrixes_of_4_functions[0])
print("\nΜέσος όρος confusion matrix για τα δοκιμασμένα n=[1,2,3,5,10] της Συνάρτησης 2",confusion_matrixes_of_4_functions[1])
print("\nΜέσος όρος confusion matrix για τα δοκιμασμένα n=[1,2,3,5,10] της Συνάρτησης 3: ",confusion_matrixes_of_4_functions[2])
print("\nΜέσος όρος confusion matrix για τα δοκιμασμένα n=[1,2,3,5,10] της Συνάρτησης 4: ",confusion_matrixes_of_4_functions[3])

print("\nΜέσος όρος όλων των Metrics για τα δοκιμασμένα n = [1,2,3,5,10] για τη Συνάρτηση 1: ",metrics_array_of_4_functions[0])
print("\nΜέσος όρος όλων των Metrics για τα δοκιμασμένα n = [1,2,3,5,10] για τη Συνάρτηση 2:",metrics_array_of_4_functions[1])
print("\nΜέσος όρος όλων των Metrics για τα δοκιμασμένα n = [1,2,3,5,10] για τη Συνάρτηση 3:",metrics_array_of_4_functions[2])
print("\nΜέσος όρος όλων των Metrics για τα δοκιμασμένα n = [1,2,3,5,10] για τη Συνάρτηση 4:",metrics_array_of_4_functions[3])


#print("Real ratings", real_ratings)
real_ratings=real_ratings[0:int(len(real_ratings)/5)]
print("\nTotal predictions", len(real_ratings))
print("Ratings that had no neighbours and could not predict the rating: ", test_ratings-len(real_ratings))
   
end_time=time.time() 
print("\nTotal seconds:", int(end_time-start_time))


    






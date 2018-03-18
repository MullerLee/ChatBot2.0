'''
   Matrix Equation Solver
   A matrix equation is like this, and we want to find the vector (x1,x2,x3) that make the variance of
   [zi] to reach a relative small value while the average of it is as large as possible
   ps: x1+x2+x3=10
   __            __   __  __    __   __
   |  a1  b1  c1  |   | x1 |    |  z1 |
   |  a2  b2  c2  | X | x2 | =  |  z2 |
   |  ...   ...   |   |_x3_|    | ... |
   |  an  bn  cn  |             |  zn |
   |__          __|             |_   _|
   the function returns the value of a list with elements of best x1, x2 and x3
   developed by Manfred Lee ( Xingchen Lee ) Mar 4th, 2018
'''

def matrix_equation_solver( L1R,L1W,L2R,L2W,L3R,L3W ):
    eq_s_A=0
    eq_s_B=0
    eq_s_C=0

    z_Ave_2=0
    z_S2_total=0
    z_S2=[1000]
    eq_z=[None]*5

    eq_s_X=[0]
    eq_s_Y=[0]
    eq_s_Z=[0]
    Ave=[0]

    list_divi1=[None]*5
    list_divi2=[None]*5
    list_divi3=[None]*5

    eq_s_count=0
    while eq_s_count<5:
        list_divi1[eq_s_count]=L1R[eq_s_count]-L1W[eq_s_count]
        list_divi2[eq_s_count]=L2R[eq_s_count]-L2W[eq_s_count]
        list_divi3[eq_s_count]=L3R[eq_s_count]-L3W[eq_s_count]
        eq_s_count=eq_s_count+1

    j=0
    while j<5:
        eq_s_A=list_divi1[j]+eq_s_A
        eq_s_B=list_divi2[j]+eq_s_B
        eq_s_C=list_divi3[j]+eq_s_C
        j=j+1

    eq_s_x1=0
    eq_s_x2=0
    eq_s_x3=10
    while eq_s_x1<=10:
        while eq_s_x2<=10-eq_s_x1:
            eq_s_x3=10-eq_s_x2-eq_s_x1
            i=0
            z_S2_total=0
            z_Ave_2=(eq_s_x1*eq_s_A+eq_s_x2*eq_s_B+eq_s_x3*eq_s_C)/5
            while i<5:
                eq_z[i]=eq_s_x1*list_divi1[i]+eq_s_x2*list_divi2[i]+eq_s_x3*list_divi3[i]
                z_S2_total=z_S2_total+(eq_z[i]-z_Ave_2)*(eq_z[i]-z_Ave_2)
                i=i+1
            eq_s_x2=eq_s_x2+1
            if(z_S2_total/5)<0.8:
                z_S2.append(z_S2_total/5)
                eq_s_X.append(eq_s_x1)
                eq_s_Y.append(eq_s_x2)
                eq_s_Z.append(eq_s_x3)
                Ave.append(z_Ave_2)
        eq_s_x1=eq_s_x1+1
        eq_s_x2=0
        eq_s_x3=10-eq_s_x2-eq_s_x1

    eq_s_a=0
    eq_s_b=0
    eq_s_c=0
    
    Ave_cache=0
    eq_s_count_2=0

    while eq_s_count_2<len(z_S2):
        if Ave_cache<Ave[eq_s_count_2]:
            eq_s_a=eq_s_X[eq_s_count_2]
            eq_s_b=eq_s_Y[eq_s_count_2]
            eq_s_c=eq_s_Z[eq_s_count_2]
            Ave_cache=Ave[eq_s_count_2]
        eq_s_count_2=eq_s_count_2+1

    return([eq_s_a,eq_s_b,eq_s_c])


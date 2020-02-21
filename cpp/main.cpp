/*
 * simplegraph.cpp
 *
 *  Created on: 26 Feb 2014
 *      Author: Tim Evans & Jonas Scholz
 */

#include "simplegraph.h"
#include <random>
#include <vector>
#include <stdlib.h>
#include <stdio.h>
#include <iostream>
#include <iomanip>
#include <fstream>
#include <array>
//#include <set>

using namespace std;

int main()
{
    string method = "task3";
    //TODO: verify method is valid str
    int nr_vertices = 5000;
    int max_m = 16;
    int m = 5;
    float q = 0.7;

    float qs [] = {0.1, 0.5, 0.95, 0.99};
    bool writeon = true;
    
    // For varying m:
    //for(int m = 1; m <= max_m; m = m*2){
        
    // For varying q:
    
    for (float q : qs){
    //for (int k = 0; k<number_qs; k++){
        // set up initial graph
        simplegraph g;
        g.addVertex();
        g.addVertex();
        g.addEdge(0, 1);
        

        // add vertices and connect them according to the random preferential attachment algorithm
        
        for (int i = 0; i < nr_vertices; i++) {

        
        int random_vertex = 0;
            
            for (int j = 0; j < m; j++){
                
                if (method == "task1"){
                    random_vertex = g.getRandomVertexPref();
                    
                }
                else if (method == "task2"){
                    random_vertex = g.getRandomVertexUniform();
                }
                else if (method == "task3"){
                    // choose initial v0
                    int vl = g.getRandomVertexUniform();
                    //cout << "v0 = " << vl << endl;
                    int l = -1;
                    bool endwalk = false;
                    //vl = g.getRandomNeighbour(vl);
                    //cout << "vl = " << vl << endl;
                    
                    while(!endwalk){
                        vl = g.getRandomNeighbour(vl);
                        endwalk = g.endwalk(q);
                        l ++;
                    }
                    random_vertex = vl; 
                    
                }
                else{
                    //cout<< "Please choose method =rng taski for i = 1,2,3" << endl;
                }
                int new_vertex = g.addVertex();
                g.addEdgeSlowly(new_vertex, random_vertex);
                //cout << "new vertex " <<new_vertex << " has " << g.v2v[new_vertex].size() << " neighbours" << endl;
            }
        }
        
        
        vector<int> dd = g.getDegreeDistribution();
        
        
        if (writeon){
            
            string fPathData = "../../data/";
            string networkDataNameStr;
            string distributionNameStr;
            //write network
            
            // define name of data file
            if (method == "task3"){
                networkDataNameStr = fPathData + method + "_network_N"+to_string(nr_vertices) + "_m" + to_string(m) + "_q" + to_string(q) + ".txt";
                distributionNameStr = fPathData + method + "_distribution_N"+to_string(nr_vertices) + "_m" + to_string(m) + "_q" + to_string(q) + ".txt";
            }
            else{
                networkDataNameStr = fPathData + method + "_network_N"+to_string(nr_vertices) + "_m" + to_string(m) + ".txt";
                distributionNameStr = fPathData + method + "_distribution_N"+to_string(nr_vertices) + "_m" + to_string(m) + ".txt";
            }
            
            char *networkDataName = &networkDataNameStr[0];
            g.write(networkDataName);
            
            //write distribution
            char *distributionName = &distributionNameStr[0];
            g.writeDistribution(distributionName, dd);
        }
    }
    
    return 0;
}

// Constructor
simplegraph::simplegraph(){
	}

	/*
	 * Adds a new vertex with no stubs.  
	 * Vertices are given an index starting from 0
	 * Returns the index of new vertex (= number of vertices -1)
	 */
	int
	simplegraph::addVertex(){
	    //v2v.push_back(set<int>());
		//vector<int> blankvector;
		v2v.push_back(vector<int>() );
		return v2v.size()-1;
	}

    /*
     * Returns random index of a vertex by pure preferential attachment/
     */
    
	int simplegraph::getRandomVertexPref(){
        //return rand() % v2v.size();
        // Pick random edge from public attachments vector
        std::random_device dev;
        std::mt19937 rng(dev());
        std::uniform_int_distribution<std::mt19937::result_type> dist(0, attachments.size() - 1);
        //cout << dist(rng);
        //cout << "attachment size: " << attachments.size() << endl;
        return attachments[dist(rng)];
    }
    
    int simplegraph::getRandomVertexUniform(){
        // Pick a random vertex from the set of existing vertices.
        std::random_device dev;
        std::mt19937 rng(dev());
        std::uniform_int_distribution<std::mt19937::result_type> dist(0, v2v.size() - 1);
        //cout << "v0 = " << dist(rng) << " max vertex = " << v2v.size() - 1 << endl;
        return dist(rng);
    }
    
    bool simplegraph::endwalk(float q){
        std::random_device rd;
        std::default_random_engine rng(rd());
        std::uniform_real_distribution<double> dist(0.0,1.0);
        float random_nr = dist(rng);

        if (random_nr > q){
            return true;
        }
        return false;
    }


	/**
	 * Adds a new edge from existing vertices s and t.
	 * No checks on vertex indices performed.
	 * No check for multiple edges of self-loops.
	 */
	void
	simplegraph::addEdge(int s, int t){
		v2v[s].push_back(t);
		v2v[t].push_back(s);
		// This version is for set based structure
		//		v2v[s].insert(t);
		//		v2v[t].insert(s);
        attachments.push_back(s);
        attachments.push_back(t);
	}

	
	/**
	 * Adds a new edge from existing vertices s and t.
	 * Checks on vertex indices and increases size if needed.
	 * Will not add self-loops.
	 * Muliple edges may be added depedning on behaviour of addedge(s,t) method.
	 * Returns negative if self-loop attempted, 0 if OK.
	 */
	int
	simplegraph::addEdgeSlowly(int s, int t){
		if (s==t) return -1;
		int maxSize=max(s,t)+1;
		if (v2v.size()<maxSize){
			v2v.resize(maxSize);
		}
		addEdge(s,t);
		return 0;
	}
	/**
	 * Fetches the n-th neighbour of vertes s
	 * Input
	 * s index of vertex whose neighhbour is required
	 * n require n-th neighbour
	 * Returns
	 * index of neighbour
	 */
	int
	simplegraph::getNeighbour(int s, int n){
		return v2v[s][n]; // is notation correct?
	};
    
    int simplegraph::getRandomNeighbour(int v0){
        int nrNeighbours = v2v[v0].size();
        //cout << "number of neighbours = " << nrNeighbours << endl;
        //cout << v2v[v0][0] <<endl;
        int n = 0;
        n = rand() % nrNeighbours;
        
        //cout << "n = " << n <<endl;
        return v2v[v0][n];
        //return getNeighbour(v0, n);
    }

	/**
	 * Returns the total number of stubs.
	 * Stubs are one end of a vertex so this is double the number of edges.
	 * Note that this is currently slow as it sums the degrees.
	 * Would be better to maintain a running total updated when addedge is called.
	 */
	int
	simplegraph::getNumberStubs(){
		int stubs=0;
		for (int v=0; v<v2v.size(); v++) stubs+=getVertexDegree(v);
		return stubs;
	};

	/**
	 * Returns the total number of edges.
	 * Note that this is currently slow as it sums the degrees.
	 * Would be better to maintain a running total updated when addedge is called.
	 */
	int
	simplegraph::getNumberEdges(){
		return getNumberStubs()/2;
	};

	/**
	 * Returns number of vertices.
	*/
	int
	simplegraph::getNumberVertices(){
		return v2v.size();
	};

	/**
		 * Returns the degree of vertex s
		 * Input
		 * s index of vertex whose neighhbour is required
		 * Returns
		 * degree of vertex
		 */
	int
	simplegraph::getVertexDegree(int s){
		return v2v[s].size();
	};

	/**
	* Returns a vector if integers with the degree distribution.
	* So if we call with
	* vector<int> dd=getDegreeDistribution()
	* then dd[k] is the number of vertices of degree[k]
	* and (dd.size()-1) is the largest degree in the network
	*/
	vector<int>
	simplegraph::getDegreeDistribution(){
		vector<int> dd;
		for (int v=0; v<getNumberVertices(); v++){	
			int k= getVertexDegree(v);
			if (dd.size()<=k){
				dd.resize(k+1); // vector must have size equal to maximum degree stored +1 as starts from k=0
			}
			dd[k]++;
		}
		return dd;
	}

	void
	simplegraph::write(char *outFile) {
	  ofstream fout(outFile);
	  if (!fout) {
	      cerr << "Can't open output file " << outFile << endl;
	      exit(1);
	  }
	  write(fout) ;
	  fout.close();
	}

	/**
	 * Output tab separated edge list of graph with no header line.
	 * Useful for some packages.
	 */
	void
	simplegraph::write(ostream & fout) {write(fout, false);}

	/**
	 * Output tab separated edge list of graph with optional header line.
	 * Needs ostream for output (e.g. cout) and true (false) if want header line
	 */
	void
	simplegraph::write(ostream & fout, bool labelOn) {
		if (labelOn) {
			fout << "v1 \t v2" << endl;
		}
		int source,target=-1;
		for (int source=0; source<getNumberVertices(); source++)
			for (int n=0; n<getVertexDegree(source); n++)
			{
				target = getNeighbour(source, n); 
				if (source<target) {
					fout << source << "\t" << target << endl;
				}
			}
	}
	
	void
	simplegraph::writeDistribution(char *outFile, vector<int> dd) {
	  ofstream fout(outFile);
      
      // Catch Exception
	  if (!fout) {
	      cerr << "Can't open output file " << outFile << endl;
	      exit(1);
	  }
	  
	  //
	  
	  for (int i = 0; i < dd.size(); i++){
          fout << i << "," << dd[i] << endl;
        }int source,target=-1;
	
	  fout.close();
	}

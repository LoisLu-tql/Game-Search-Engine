package cn.loix.test;

import org.apache.lucene.analysis.Analyzer;
import org.apache.lucene.document.Document;
import org.apache.lucene.index.DirectoryReader;
import org.apache.lucene.index.IndexReader;
import org.apache.lucene.queryparser.classic.MultiFieldQueryParser;
import org.apache.lucene.queryparser.classic.QueryParser;
import org.apache.lucene.search.IndexSearcher;
import org.apache.lucene.search.Query;
import org.apache.lucene.search.ScoreDoc;
import org.apache.lucene.search.TopDocs;
import org.apache.lucene.store.Directory;
import org.apache.lucene.store.FSDirectory;
import org.junit.Test;
import org.wltea.analyzer.lucene.IKAnalyzer;

import java.nio.file.Paths;

public class TestSearch {

    @Test
    public void searchTest() throws Exception {
        Analyzer analyzer = new IKAnalyzer();

//        QueryParser queryParser = new QueryParser(f={"game_name", "game_intro"}, analyzer);
        String[] query_fields = {"game_name", "game_intro", "game_tag"};
        MultiFieldQueryParser queryParser = new MultiFieldQueryParser(query_fields, analyzer);
        Query query = queryParser.parse("足球");

        Directory directory = FSDirectory.open(Paths.get("../indexlib"));

        IndexReader indexReader = DirectoryReader.open(directory);

        IndexSearcher indexSearcher = new IndexSearcher(indexReader);
        TopDocs topDocs = indexSearcher.search(query, 10);
        System.out.println("total num:" + topDocs.totalHits);
        ScoreDoc[] scoreDocs = topDocs.scoreDocs;

        if(scoreDocs != null){
            for(ScoreDoc scoreDoc : scoreDocs){
                int docID = scoreDoc.doc;
                Document doc = indexSearcher.doc(docID);
                System.out.println("------result:" + doc.get("game_name"));
            }
        }

    }
}

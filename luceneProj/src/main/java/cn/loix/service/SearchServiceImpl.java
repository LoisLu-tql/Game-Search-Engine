package cn.loix.service;

import cn.loix.pojo.Game;
import cn.loix.pojo.SearchResults;
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
import org.apache.lucene.search.highlight.*;
import org.apache.lucene.store.Directory;
import org.apache.lucene.store.FSDirectory;
import org.springframework.stereotype.Service;
import org.springframework.util.StringUtils;
import org.wltea.analyzer.lucene.IKAnalyzer;

import java.io.IOException;
import java.nio.file.Paths;
import java.util.ArrayList;
import java.util.List;

@Service
public class SearchServiceImpl implements SearchService {

    public final static Integer PAGE_SIZE = 15;

    @Override
    public SearchResults query(String queryStr, String searchWay, Integer page) throws Exception {
        long page_begin = System.currentTimeMillis();

        SearchResults searchResults = new SearchResults();
        List<Game> gameList = new ArrayList<>();
        Integer start = (page - 1) * PAGE_SIZE;
        Integer end = page * PAGE_SIZE;

        Analyzer analyzer = new IKAnalyzer();

        QueryParser queryParser = null;
        if(searchWay.equals("all")){
            //全文检索
            String[] fields = {"game_name", "game_src", "game_tag",
                    "game_intro", "game_developer", "game_publisher", "game_birth"};
            queryParser = new MultiFieldQueryParser(fields, analyzer);
        } else{
            queryParser = new QueryParser("game_name", analyzer);
        }

        Query query = null;
        long search_begin = System.currentTimeMillis();
        if(StringUtils.isEmpty(queryStr)){
            query = queryParser.parse("*:*");
        } else{
            query = queryParser.parse(queryStr);
        }

        Directory directory = FSDirectory.open(Paths.get("../indexlib"));
        IndexReader indexReader = DirectoryReader.open(directory);
        IndexSearcher indexSearcher = new IndexSearcher(indexReader);
        TopDocs topDocs = indexSearcher.search(query, end);
        ScoreDoc[] docs = topDocs.scoreDocs;
        long search_end = System.currentTimeMillis();

        for(int i=start; i<(end>topDocs.totalHits?topDocs.totalHits:end); i++){
            Document doc = indexReader.document(docs[i].doc);
            String name_str = Highlight(query, analyzer, "game_name", doc.get("game_name"));
            String intro_str = Highlight(query, analyzer, "game_intro", doc.get("game_intro"));


            Game game = new Game();
            game.setId(Integer.parseInt(String.valueOf(doc.get("id"))));
            game.setGame_tag(doc.get("game_tag"));
            game.setGame_src(doc.get("game_src"));
            game.setGame_publisher(doc.get("game_publisher"));
            game.setGame_name(name_str == null ? doc.get("game_name") : name_str);
            game.setGame_link(doc.get("game_link"));
            game.setGame_intro(intro_str == null | searchWay.equals("topic") ? doc.get("game_intro") : intro_str);
            game.setGame_img(doc.get("game_img"));
            game.setGame_developer(doc.get("game_developer"));
            game.setGame_birth(doc.get("game_birth"));
            gameList.add(game);
        }

        searchResults.setGameList(gameList);
        searchResults.setPage_now(page);
        searchResults.setTotal_count(topDocs.totalHits);
        searchResults.setPage_count(
                topDocs.totalHits % PAGE_SIZE > 0 ?
                        (topDocs.totalHits / PAGE_SIZE) + 1 : topDocs.totalHits / PAGE_SIZE
        );
        searchResults.setSearch_time(search_end-search_begin);
        searchResults.setSearch_way(searchWay);

        indexReader.close();

        long page_end = System.currentTimeMillis();
        searchResults.setPage_time(page_end-page_begin);
        return searchResults;
    }

    static String Highlight(Query query, Analyzer analyzer, String fieldName, String fieldContent)
            throws InvalidTokenOffsetsException, IOException {
        Highlighter highlighter = new Highlighter(
                new SimpleHTMLFormatter("<font color='red'>", "</font>"), new QueryScorer(query));
        return highlighter.getBestFragment(analyzer, fieldName, fieldContent);
    }
}

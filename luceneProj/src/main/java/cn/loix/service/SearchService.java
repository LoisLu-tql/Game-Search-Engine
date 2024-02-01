package cn.loix.service;

import cn.loix.pojo.SearchResults;

public interface SearchService {
    public SearchResults query(String queryStr, String searchWay, Integer page) throws Exception;
}

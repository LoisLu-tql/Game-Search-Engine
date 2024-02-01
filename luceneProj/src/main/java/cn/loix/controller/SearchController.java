package cn.loix.controller;

import cn.loix.pojo.SearchResults;
import cn.loix.service.SearchService;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Controller;
import org.springframework.ui.Model;
import org.springframework.util.StringUtils;
import org.springframework.web.bind.annotation.RequestBody;
import org.springframework.web.bind.annotation.RequestMapping;

@Controller
@RequestMapping("/search")
public class SearchController {
    @Autowired
    private SearchService searchService;

    @RequestMapping
    public String query(String queryStr, String searchWay, Integer page, Model model) throws Exception{
        if(StringUtils.isEmpty(page)){
            page = 1;
        }
        if(page <= 0){
            page = 1;
        }
        if(searchWay == null){
            searchWay = "all";
        }

        SearchResults searchResults = searchService.query(queryStr, searchWay, page);

        model.addAttribute("queryStr", queryStr);
        model.addAttribute("searchWay", searchWay);
        model.addAttribute("page", page);
        model.addAttribute("result", searchResults);
        return "search";
    }
}

package com.example.demo.controller;

import org.springframework.stereotype.Controller;
import org.springframework.ui.Model;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PathVariable;
import org.springframework.web.bind.annotation.RequestMapping;

@Controller
@RequestMapping
public class DemoController {
    @GetMapping("/")
    public String index(Model model){
        model.addAttribute("id",1);
        return "index";
    }

    @GetMapping("/{id}")
    public String next(Model model, @PathVariable("id") Integer id){
        model.addAttribute("id", id);
        return "index";
    }
}

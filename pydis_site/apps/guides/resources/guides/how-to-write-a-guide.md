Title: How to Write a Guide
ShortDescription: Learn how to write a guide for this website
Contributors: ks129

When you are interested about how to write guide for this site (like this), then you can learn about it here.
PyDis use Markdown files for guides, but these files have some small differences from standard Markdown (like defining HTML IDs and classes).

## [Getting Started](#getting-started){: id="getting-started" }
First, you have to have a good idea, that match with PyDis theme. We can't accept guides like *How to bake a cake*,
*How to lose weigth*. These doesn't match with PyDis theme and will be declined. Most of guides theme should be server and Python, but there can be some exceptions, when they are connected with PyDis.
Best way to find out is your idea good is to discuss about it in #dev-core channel. There can other peoples give their opinion about your idea. Even better, open issue in site repository first, then PyDis staff can see it and approve/decline this idea.
It's good idea to wait for staff decision before starting to write guide to avoid case when you write a long long guide, but then this don't get approved.

To start with contributing, you should read [how to contribute to site](https://pythondiscord.com/pages/contributing/site/).
You should also read our [Git workflow](https://pythondiscord.com/pages/contributing/working-with-git/), because you need to push your guide to GitHub.

## [Creating a File](#creating-a-file){: id="creating-a-file" }
All guides is located at `site` repository, in `pydis_site/apps/guides/resources/guides`. Under this is root level guides (.md files) and categories (directories). Learn more about categories in [categories section](#categories).

At this point, you will need your guide name for filename. Replace all your guide name spaces with `-` and make all lowercase. Save this as `.md` (Markdown) file. This name (without Markdown extension) is path of guide in URL.

## [Markdown Metadata](#markdown-metadata){: id="markdown-metadata" }
Guide files have some required metadata, like title, contributors, description, relevant pages. Metadata is first thing in file, YAML-like key-value pairs:

```md
Title: My Guide
ShortDescription: This is my short description.
Contributors: person1
              person2
              person3
RelevantLinks: url1
               url2
               url3
RelevantLinkValues: Text for url1
                    Text for url2
                    Text for url3

Here comes content of guide...
```

You can read more about Markdown metadata [here](https://python-markdown.github.io/extensions/meta_data/).

### Fields
- **Name:** Easily-readable name for your guide.
- **Short Description:** Small, 1-2 line description that describe what your guide explain.
- **Contributors:** All who have contributed to this guide. One person per-line, and they **have to be at same level**. When you edit guide, add your name to there.
- **Relevant Links and Values:** Links that will be shown at right side. Both key's values have to be at same level, just like for contributors field.

## [Content](#content){: id="content" }
For content, mostly you can use standard markdown, but there is a few addition that is available.

### HTML classes and IDs
To provide HTML classes and/or IDs, this use `{: id="myid" class="class1 class2" }`. When using it at header, place this **right after** title, no space between them. For mutliline items, place them next line after end of block. You can read more about it [here](https://python-markdown.github.io/extensions/attr_list/).

## [Categories](#categories){: id="categories" }
To have some systematic sorting of guides, site support guides categories. Currently this system support only 1 level of categories. Categories live at `site` repo in `pydis_site/apps/guides/resources/guides` subdirectories. Directory name is path of category in URL. Inside category directory, there is 1 file required: `_info.yml`. This file need 2 key-value pairs defined:

```yml
name: Category name
description: Category description
```

Then all Markdown files in this folder will be under this category.

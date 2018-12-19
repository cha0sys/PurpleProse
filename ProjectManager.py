# -*- coding: utf-8 -*-
# TODO handler for reorder

import os
from pathlib import Path
import sqlite3
from datetime import datetime

import logging
logging.basicConfig(filename='PP_runtime.log',level=logging.INFO)

class ProjectManager (object):
    conn = None
    ppath = Path('./Projects/')
    pdb = Path('Project.ppp')

    def __init__(self,parent=None):
        super(ProjectManager , self).__init__()
        self.parent = parent
        self.conn = sqlite3.connect(':memory:')
        self.conn.row_factory = sqlite3.Row

    def NewProject(self,title='New Project',dbfile=':memory:'):
        # make a new database for the project
        #check:ok
        cur = self.conn.cursor()
        logging.info("Creating database in memory...")
        cur.execute('create table project (id integer primary key,title,modified,editstatus,lastopensceneid);')
        logging.info("PROJECT")
        cur.execute('create table entities (id integer primary key,name,desc,type);')
        logging.info("ENTITIES")
        cur.execute('create table entity_aliases (entity_id, alias_id integer primary key, alias);')
        logging.info("ENTITY_ALIASES")
        cur.execute('create table related_entities (entity_id,related_id);')
        logging.info("RELATED_ENTITIES")
        cur.execute('create table entity_categories (id integer primary key, singular, plural, parent_id);')
        logging.info("ENTITY_CATEGORIES")
        cur.execute('create table scenes (id integer primary key,displayorder,title,contents,filepath,modified,editstatus);')
        logging.info("SCENES")
        cur.execute('create table edit_statuses (id integer primary key, status);')
        logging.info("EDIT_STATUSES")
        cur.execute('create table scene_entities (scene_id,entity_id);')
        logging.info("SCENE_ENTITIES")
        cur.execute('create table chapters (id integer primary key,title,displayorder);')
        logging.info("CHAPTERS")
        cur.execute('create table chapter_scenes (chapter_id, scene_id);')
        logging.info("CHAPTER_SCENES")
        cur.execute('create table books (id integer primary key,title,displayorder);')
        logging.info("BOOKS")
        cur.execute('create table book_chapters (book_id,chapter_id);')
        logging.info("BOOK_CHAPTERS")
        cur.execute('create table project_books (project_id,book_id);')
        logging.info("PROJECT_BOOKS")
        logging.info("Committing table creation...")
        self.conn.commit()
        logging.info("Tables created.")

        # insert starting records
        logging.info("Generating path for default scene file...")
        self.pdb = Path(dbfile)
        logging.info(self.pdb)
        self.ppath = Path('./Projects/', title)
        logging.info(self.ppath)
        scenepath = str(self.ppath.joinpath('Book_1/Chapter_1/0001 - Scene_1.md'))
        logging.info(scenepath)
        logging.info("Creating default records...")
        cur.executemany("insert into edit_statuses values (?,?);",((0,'Draft'),(1,'Proof'),(2,'Complete')))
        logging.info("Edit statuses inserted.")
        cur.execute("insert into project values (0,?,?,0,0);", (title, datetime.now().isoformat()))
        logging.info("Base project inserted.")
        cur.execute("insert into books values (0,'Book 1',1);")
        logging.info("Default book inserted.")
        cur.execute("insert into project_books values (0,0);")
        logging.info("Default book linked to base project.")
        cur.execute("insert into chapters values (0,'Chapter 1',1);")
        logging.info("Default chapter inserted.")
        cur.execute("insert into book_chapters values (0,0);")
        logging.info("Default chapter linked to default book.")
        cur.execute("insert into scenes values (0,1,'Scene 1','It was a dark and stormy night...',?,?,0);", (scenepath,datetime.now().isoformat()))
        logging.info("Default scene inserted.")
        cur.execute("insert into chapter_scenes values (0,0);")
        logging.info("Default scene linked to default chapter.")
        cur.execute("insert into entity_categories values (0,'Metadata','Metadata',NULL);")
        logging.info("Root metadata note inserted.")
        cur.executemany("insert into entity_categories values (NULL,?,?,0);", \
            (('Character','Characters'),('Faction','Factions'),('Location','Locations'), \
             ('Item','Items'),('Note','Notes'),('Research','Research'),('Other','Other')))
        logging.info("Default metadata categories inserted.")
        logging.info("Committing default record insertion...")
        self.conn.commit()
        logging.info("Default records created.")

        # close the cursor but leave the connection for later
        cur.close()
        if dbfile != ':memory:':
            logging.info("Saving project DB to disk")
            logging.info(self.ppath)
            logging.info(self.pdb)
            self.ppath.mkdir(parents=True,exist_ok=True)
            ppdb = self.ppath / self.pdb
            logging.info(ppdb)
            with sqlite3.connect(ppdb) as dbf:
                self.conn.backup(dbf)
                logging.info("Project saved to disk.")

    def GetLastOpenScene(self):
        # returns the id of the most recently modified scene.
        #check:ok
        try:
            cur = self.conn.cursor()
            logging.info("Getting first scene...")
            cur.execute("select id,modified from scenes where id=0;")
            cls = cur.fetchone()
            logging.info(cls)
            logging.info("Getting modify timestamp of first scene...")
            logging.info(cls['modified'])
            cldt = datetime.fromisoformat(cls['modified'])
            logging.info(cldt)
            for csdr in cur.execute("select id,modified from scenes;"):
                logging.info("Scene %i" % csdr['id'])
                csdt = datetime.fromisoformat(csdr['modified'])
                logging.info(csdt)
                if csdt > cldt:
                    cls = csdr
            logging.info(cls['id'])
            ret = cls['id']
        except Exception as err:
            logging.error("Couldn't get last open Scene ID!")
            logging.error(err)
            ret = False
        finally:
            cur.close()
        return ret

    def SaveProject(self):
        # save last open scene id to DB
        #check:unverified
        cur = self.conn.cursor()
        logging.info("Storing most recent scene ID.")
        losid = self.GetLastOpenScene()
        logging.info(losid)
        cur.execute("select * from project;")
        pc = cur.fetchone()
        pcd = dict(zip(pc.keys(),tuple(pc)))
        logging.info(pcd)
        try:
            cur.execute("update or replace project set lastopensceneid = :losid where id = 0;", {'losid':losid})
            logging.info("Most recent scene ID stored.")
        except sqlite3.Error as e:
            logging.error('Error updating most recent scene ID in PROJECT table.')
            logging.error(e)
        finally:
            self.conn.commit()
        # save all scenes to DB and files
        logging.info("Saving scenes to disk.")
        try:
            for s in cur.execute("select id from scenes;"):
                self.SaveSceneToFile(s['id'])
            logging.info("Scenes saved.")
        except Exception as err:
            logging.error("Couldn't save scenes!")
            logging.error(err)
        finally:
            cur.close()

        # saves the open project to the disk
        logging.info("Saving project DB to disk")
        logging.info(self.pdb)
        with sqlite3.connect(self.ppath / self.pdb) as dbf:
            self.conn.backup(dbf,pages=1)
        logging.info("Project saved to disk.")

    def OpenProject(self,dbpath):
        # loads a project db file into memory
        # returns the id of the last open scene
        #check:unverified
        self.ppath = Path(dbpath).parent
        self.pdb = Path(dbpath).name
        logging.info("Project paths set.")
        try:
            self.conn = sqlite3.connect(':memory:')
            self.conn.row_factory = sqlite3.Row
            dbf = sqlite3.connect(dbpath)
            logging.info("Loading DB to memory.")
            dbf.backup(self.conn)
            dbf.close()
        except Exception as err:
            logging.error("Couldn't load DB to memory!")
            logging.error(err)
        try:
            logging.info("Loading scenes from disk...")
            self.ReloadAllScenes()
        except Exception as err:
            logging.error("Could not load scenes!")
            logging.error(err)

        logging.info("Getting the last open scene id...")
        losid = self.GetLastOpenScene()
        logging.info(losid)
        return losid

    def GetBookTree(self):
        # returns a dict of lists of dicts representing the Books subtree
        #check:ok
        logging.info("Getting Books subtree...")
        booktree = {}
        books = []
        chapters = []
        scenes = []
        cur = self.conn.cursor()
        for r in cur.execute("select id,title,displayorder,chapter_id from scenes join chapter_scenes where scenes.id = chapter_scenes.scene_id order by displayorder asc;"):
            scenes.append({'order':r['displayorder'],'title':r['title'],'id':r['id'],'chapter':r['chapter_id'],'type':'Scene'})
        for r in cur.execute("select id,title,displayorder,book_id from chapters join book_chapters where chapters.id=book_chapters.chapter_id order by displayorder asc;"):
            chapters.append({'order':r['displayorder'],'title':r['title'],'id':r['id'],'book':r['book_id'],'type':'Chapter'})
        for r in cur.execute("select id,title,displayorder from books order by displayorder asc;"):
            books.append({'order':r['displayorder'],'title':r['title'],'id':r['id'],'type':'Book'})

        booktree = {'Books':books,'Chapters':chapters,'Scenes':scenes}
        logging.info(booktree)
        cur.close()
        return booktree

    def GetMetaTree(self):
        # returns a list of dicts representing the Metadata subtree
        #check:ok
        logging.info("Getting Metadata subtree...")
        metatree = {}
        types = []
        entities = []
        cur = self.conn.cursor()
        for r in cur.execute("select id,name,type from entities order by type desc, name desc;"):
            entities.append({'id':r['id'],'name':r['name'],'cat_id':r['type'],'type':'Metadata Entry'})
        for r in cur.execute("select id,plural,parent_id from entity_categories order by id asc;"):
            types.append({'id':r['id'],'parent':r['parent_id'],'label':r['plural'],'type':'Metadata Type'})

        metatree = {'Types':types,'Entries':entities}
        logging.info(metatree)
        cur.close()
        return metatree

    def CloseProject(self):
        # close down the project and terminate all connections cleanly
        #check:unverified
        logging.info("Project Close requested.")
        self.SaveProject()
        self.conn.commit()
        self.conn.close()
        logging.info("Closed.")

    def RenameProject(self,newname):
        # renames the project in the database.
        # regenerates the project paths and files when done.
        logging.info("Project Rename requested.")
        try:
            self.ReloadAllScenes()
            cur = self.conn.cursor()
            cur.execute("update project set title=:nn where id=0;",{'nn':newname})
            self.conn.commit()
            self.RegenProjectFiles()
            self.RegenAllSceneFiles()
        except Exception as e:
            logging.error("Could not rename project!")
            logging.error(e)
        finally:
            cur.close()

    def RegenProjectFiles(self):
        # renames DB file, updates project paths accordingly, deletes old DB
        oldpath = self.ppath
        #olddb = self.pdb
        try:
            pt = self.GetProjectData()['title']
            self.pdb = Path(pt + '.ppp')
            self.ppath = Path('./Projects/' + pt)
            os.deltree(oldpath)
            self.BackupDBtoFile(self.ppath / self.pdb)
            self.RegenAllSceneFiles()
        except Exception as e:
            logging.error("Couldn't rename project!")
            logging.error(e)

    def ReloadAllScenes(self):
        # for each scene, reload its contents from its MD files.
        logging.info("Reloading all scenes...")
        try:
            cur = self.conn.cursor()
            for s in cur.execute("select id from scenes;"):
                logging.info("Reloading scene...")
                logging.info(s)
                self.LoadScene(s['id'])
        except Exception as err:
            logging.error("Couldn't reload scenes!")
            logging.error(err)
        finally:
            cur.close()
            logging.info("All scenes reloaded from disk.")

    def RegenAllSceneFiles(self):
        # for each scene, regenerates its file path and re-exports, deleting the old ones.
        try:
            cur = self.conn.cursor()
            for s in cur.execute("select id from scenes;"):
                self.RegenSceneFilePath(s['id'])
        except Exception as e:
            logging.error("Could not regen scene files!")
            logging.error(e)
        finally:
            cur.close()

    def BackupDBtoFile(self,dbpath):
        # writes the DB to disk
        # saves the open project to the disk
        logging.info("Saving project DB to disk...")
        logging.info(dbpath)
        try:
            with sqlite3.connect(dbpath) as dbf:
                self.conn.backup(dbf,pages=1)
            logging.info("Project saved to disk.")
        except Exception as e:
            logging.error("Couldn't back up DB to disk!")
            logging.error(e)

    def NewBook(self,title):
        # creates a new book
        # returns book id
        #check:unverified
        cur = self.conn.cursor()
        cur.execute("insert into books values (NULL,?);",title)
        cur.execute("select id from books where title=?;",title)
        bk = cur.fetchone()['id']
        cur.execute("insert into project_books values (0,?);",bk)
        self.conn.commit()
        cur.close()
        return bk

    def RenameBook(self,bid,newtitle):
        # renames a book in the DB
        # caller should update project tree
        cur = self.conn.cursor()
        try:
            cur.execute("update books set title=:nt where id=:bid;", \
                {'bid':bid,'nt':newtitle})
            self.conn.commit()
            ret = True
        except Exception as e:
            logging.error("Could not rename book in DB!")
            logging.error(e)
            ret = False
        finally:
            cur.close()
        return ret

    def DeleteBook(self,bid):
        # deletes a book from the DB
        # raises an exception if child chapters exist
        # caller should update project tree
        logging.info("Deleting book")
        logging.info(bid)
        cur = self.conn.cursor()
        try:
            cur.execute("delete from project_books where book_id=:bid;", {'bid':bid})
            cur.execute("delete from book_chapters where book_id=:bid;", {'bid':bid})
            cur.execute("delete from books where id=:bid;", {'bid':bid})
            self.conn.commit()
            ret = True
        except Exception as e:
            logging.error("Cannot delete book!")
            logging.error(e)
            ret = False
        finally:
            cur.close()
        return ret

    def NewChapter(self,chname,bookid):
        # creates a new chapter
        # returns chapter id
        #check:unverified
        cur = self.conn.cursor()
        try:
            cur.execute("insert into chapters values (NULL,:cname);",{'cname':chname})
            cur.execute("select id from chapters where title=:cname;",{'cname':chname})
            ch = cur.fetchone()['id']
            cur.execute("insert into book_chapters values (?,?);",(bookid,ch))
            self.conn.commit()
        except Exception as e:
            logging.error("Could not create new chapter in DB!")
            logging.error(e)
            ch = None
        finally:
            cur.close()
        return ch

    def RenameChapter(self,cid,newtitle):
        # renames a chapter in the database
        # caller should update project tree
        logging.info("Chapter rename requested.")
        cur = self.conn.cursor()
        try:
            cur.execute("update chapters set title=:nt where id=:cid;", \
                {'cid':cid,'nt':newtitle})
            self.conn.commit()
            ret = True
            logging.info("Chapter rename complete.")
        except Exception as e:
            logging.error("Could not rename chapter in DB!")
            logging.error(e)
            ret = False
        finally:
            cur.close()
        return ret

    def MoveChapter(self,cid,bid):
        # changes chapter's parent book
        # caller should update project tree
        cur = self.conn.cursor()
        logging.info(cid)
        logging.info(bid)
        try:
            cur.execute("update chapter_books set book_id=:bid where chapter_id=:cid;", \
                {'cid':cid,'bid':bid})
            self.conn.commit()
            ret=True
        except Exception as e:
            logging.error("Cannot move chapter!")
            logging.error(e)
            ret=False
        finally:
            cur.close()
        return ret

    def DeleteChapter(self,cid):
        # deletes a chapter from the DB
        # raises exception if child scenes exist
        # caller should update project tree
        logging.info("Deleting chapter")
        logging.info(cid)
        cur = self.conn.cursor()
        try:
            cur.execute("delete from book_chapters where chapter_id=:cid;", {'cid':cid})
            cur.execute("delete from chapter_scenes where chapter_id=:cid;", {'cid':cid})
            cur.execute("delete from chapters where id=:cid;", {'cid':cid})
            self.conn.commit()
            ret = True
        except Exception as e:
            logging.error("Cannot delete chapter!")
            logging.error(e)
            ret = False
        finally:
            cur.close()
        return ret

    def NewScene(self,scenename,bookid,chapterid):
        # creates a new scene
        # returns the scene id
        #check:ok
        logging.info("Creating new scene...")
        try:
            cur = self.conn.cursor()
            # get the parent book and chapter titles for building the scene's filepath
            cur.execute('select title from books where id=:bid;',{'bid':bookid})
            bk = cur.fetchone()['title']
            logging.info(bk)
            cur.execute('select title from chapters where id=:cid;',{'cid':chapterid})
            ch = cur.fetchone()['title']
            logging.info(ch)

            cur.execute("""
                select max(displayorder) as latest from scenes where id in
                    (select scene_id from chapter_scenes where chapter_id=:cid);
                """, {'cid':chapterid})
            so = str(cur.fetchone()['latest'] + 1).zfill(4)
            logging.info(so)
            sfp = self.ppath / bk / ch / Path(so + ' - ' + scenename + '.md')
            logging.info(sfp)
            cur.execute("""
                insert into scenes values (NULL,?,?,'',?,?,0);
                """, (so, scenename, str(sfp), datetime.now().isoformat()))
            cur.execute("select id from scenes where title=:sn;", {'sn':scenename})
            sid = cur.fetchone()['id']
            cur.execute("insert into chapter_scenes values (?,?);",(chapterid,sid))
            self.conn.commit()
        except Exception as e:
            logging.error("Error querying DB:")
            logging.error(e)
            self.conn.rollback()
        finally:
            cur.close()
        return sid

    def SaveScene(self,scene,contents):
        # saves a scene to the db
        #check:ok
        logging.info("Saving scene to DB.")
        cur = self.conn.cursor()
        cur.execute("""
            update scenes set contents = :cnt
            where id=:sid;
            """,{'cnt':contents,'sid':scene})
        logging.info("Contents stored.")
        cur.execute("""
            update scenes set modified = :dt
            where id=:sid;
            """, {'dt':datetime.now().isoformat(),'sid':scene})
        logging.info("Timestamp updated.")
        self.conn.commit()
        logging.info("Changes committed.")
        cur.close()

    def SaveSceneToFile(self,sceneid):
        # saves a scene to file
        #check:unverified
        logging.info("Saving scene to file.")
        cur = self.conn.cursor()
        try:
            cur.execute("select contents,filepath from scenes where id = :sid;",{'sid':sceneid})
            scn = cur.fetchone()
            spath = Path(scn['filepath'])
            if spath.exists() == False:
                spath.parent.mkdir(parents=True,exist_ok=True)
            with spath.open('w') as outfile:
                outfile.write(scn['contents'])
            logging.info("%s written to disk." % str(spath))
        except Exception as err:
            logging.error("Can't save scene to disk!")
            logging.error(err)
        finally:
            cur.close()

    def RegenSceneFilePath(self,sceneid):
        # regenerate scene file path
        #check:unverified
        sd = self.GetSceneData(sceneid)
        oldpath = Path(sd['file']) # for deletion
        chapterid = self.GetSceneChapter(sceneid)
        bookid = self.GetChapterBook(chapterid)
        logging.info("Old path: %s" % str(oldpath))
        cur = self.conn.cursor()
        try:
            cur.execute('select title from books where id=:bid;',{'bid':bookid})
            bk = cur.fetchone()['title']
            cur.execute('select title from chapters where id=:cid;',{'cid':chapterid})
            ch = cur.fetchone()['title']
            sfp = self.ppath / bk / ch / Path(str(sd['order']).zfill(4) + ' - ' + sd['title'] + '.md')
            logging.info("New path: %s" % str(sfp))
            if oldpath != sfp:
                cur.execute("""
                    update scenes set filepath=:fp
                    where id=:sid;
                    """, {'fp':str(sfp), 'sid':sceneid})
                self.conn.commit()
                # delete old file
                if oldpath.exists():
                    os.remove(oldpath)
        except Exception as e:
            logging.error("Could not update DB with new path %s!" % str(sfp))
            logging.error(e)
        finally:
            cur.close()

    def OpenScene(self,scene):
        # returns the text of a scene
        #check:ok
        cur = self.conn.cursor()
        cur.execute("select contents from scenes where id=:scid;",{'scid':scene})
        r = cur.fetchone()
        if r != []:
            stxt = r['contents']
        else:
            stxt = ''
        return stxt

    def LoadScene(self,sid):
        # loads a scene into the DB from its MD file
        logging.info("Loading scene %i from file..." % sid)
        try:
            cur = self.conn.cursor()
            cur.execute("select filepath from scenes where id=:sid;",{'sid':sid})
            r = cur.fetchone()
            p = Path(r['filepath'])
            logging.info(str(p))
            contents = p.read_text()
            cur.execute("update scenes set contents=:stxt where id=:sid;",{'stxt':contents,'sid':sid})
            logging.info("Scene %i loaded." % sid)
            self.conn.commit()
            ret = True
        except Exception as e:
            logging.error("Could not load scene from file to DB!")
            logging.error(e)
            ret = False
        finally:
            cur.close()
        return ret

    def RenameScene(self,sid,newtitle):
        # renames a scene in the DB
        # caller should update project tree
        cur = self.conn.cursor()
        logging.info("Scene rename requested.")
        try:
            cur.execute("update scenes set title=:nt where id=:sid;", {'nt':newtitle,'sid':sid})
            self.conn.commit()
            logging.info("Updating scene file path...")
            self.RegenSceneFilePath(sid)
            logging.info("Saving scene to updated filepath...")
            self.SaveSceneToFile(sid)
            logging.info("Done.")
        except Exception as e:
            logging.error("Cannot rename scene!")
            logging.error(e)
        finally:
            cur.close()

    def MoveScene(self,sid,cid):
        # changes scene's parent chapter to cid
        # caller should update project tree
        cur = self.conn.cursor()
        logging.info(sid)
        logging.info(cid)
        try:
            cur.execute("update scene_chapters set chapter_id=:cid where id=:sid;", \
                {'cid':cid,'sid':sid})
            self.conn.commit()
            self.RegenSceneFilePath(sid)
            ret=True
        except Exception as e:
            logging.error("Cannot move scene!")
            logging.error(e)
            ret=False
        finally:
            cur.close()
        return ret

    def DeleteScene(self,sid):
        # deletes a scene from the DB
        # returns True if success, False if exception
        # caller should update project tree
        cur = self.conn.cursor()
        try:
            cur.execute("delete from scene_entities where scene_id=:sid;", {'sid':sid})
            cur.execute("delete from chapter_scenes where scene_id=:sid;", {'sid':sid})
            cur.execute("delete from scenes where id=:sid;", {'sid':sid})
            self.conn.commit()
            ret = True
        except Exception as e:
            logging.error("Cannot delete scene!")
            logging.error(e)
            ret = False
        finally:
            cur.close()
        return ret

    def NewEntityType(self,singular,plural,parentid):
        # creates a new entity category
        # returns the category id
        # entity_categories (id integer primary key, singular, plural, parent_id)
        #check:unverified
        cur = self.conn.cursor()
        cur.execute("insert into entity_categories values (NULL, ?,?,?);",(singular,plural,parentid))
        cur.execute("select id from entity_categories where singular=? and plural=?;"(singular,plural))
        etid = cur.fetchone()['id']
        self.conn.commit()
        cur.close()
        return etid

    def RenameEntityType(self,etid,newname):
        # renames a metadata category in the database
        # caller should update the project tree
        cur = self.conn.cursor()
        try:
            cur.execute("update entity_categories set name=:en where id=:enid;", \
                {'en':newname, 'enid':etid})
            self.conn.commit()
        except Exception as e:
            logging.error("Could not rename category!")
            logging.error(e)
        finally:
            cur.close()

    def DeleteEntityType(self,etid):
        # deletes an entity type from the database
        # caller should update the project tree
        cur = self.conn.cursor()
        try:
            cur.execute("delete from entity_categories where id=:enid;", \
                {'enid':etid})
            self.conn.commit()
        except Exception as e:
            logging.error("Could not delete category!")
            logging.error(e)
        finally:
            cur.close()

    def NewEntity(self,ent):
        # creates a new entity
        # returns entity id
        # entities (id integer primary key,name,desc,type)
        # ent is a dict with the following keys:
        # 'name','desc','type','aliases','related'
        #check:unverified
        logging.info("New Entity requested.")
        try:
            cur = self.conn.cursor()
            cur.execute("insert into entities values (NULL,:name,:desc,:type);", \
                {'name':ent['name'], 'desc':ent['desc'], 'type':ent['type']})
            cur.execute("select id from entities where name = :name;", {'name':ent['name']})
            eid = cur.fetchone()['id']
            logging.info("eid: %i" % eid)
            # new entity, so no aliases or relations yet
            self.conn.commit()
        except Exception as err:
            logging.error("Could not create new entity in DB!")
            logging.error(err)
            eid = None
        finally:
            cur.close()
        return eid

    def SaveEntity(self,entityid,newdata):
        # saves an entity to the db file
        # newdata is a dictionary with 5 fields:
        # 'name','aliases','related', 'type', and 'desc'
        # 'aliases' and 'related' are multi-line
        # and have one record per line.
        #check:unverified
        logging.info("Entity save requested.")
        try:
            cur = self.conn.cursor()
            logging.info("Updating ENTITIES table...")
            cur.execute("""
                    update entities
                    set name=:name,
                    type=:type,
                    desc=:desc
                    where id=:eid;
                """,{'name':newdata['name'],'type':newdata['type'],'desc':newdata['desc'],'eid':entityid})
            logging.info("ENTITIES table updated.")
            if newdata['related'] != '':
                logging.info("Updating RELATED_ENTITIES table...")
                relations = map(self.GetEntID, newdata['related'].split('\n'))
                logging.info(relations)
                for r in relations:
                    cur.execute("replace into related_entities values (:eid,:rel);", {'eid':entityid, 'rel':r})
                logging.info("RELATED_ENTITIES table updated.")
            if newdata['aliases'] != '':
                logging.info("Updating ENTITY_ALIASES table...")
                aliases = newdata['aliases'].split('\n')
                logging.info(aliases)
                for a in aliases:
                    cur.execute("replace into entity_aliases values (:eid,NULL,:alias);", {'eid':entityid, 'alias':a})
                logging.info("ENTITY_ALIASES table updated.")
            logging.info("Committing changes...")
            self.conn.commit()
            logging.info("Changes committed to database.")
        except Exception as err:
            logging.error("Couldn't save entity!")
            logging.error(err)
        finally:
            cur.close()

    def OpenEntity(self,eid):
        # returns a dictionary with entity data
        # just a convenience function for code clarity
        return self.GetEntityData(eid)

    def RenameEntity(self,eid,newname):
        # renames a metadata entry in the database
        # caller should update the project tree
        cur = self.conn.cursor()
        try:
            cur.execute("update entities set name=:en where id=:enid;", \
                {'en':newname, 'enid':eid})
            self.conn.commit()
        except Exception as e:
            logging.error("Could not rename entity!")
            logging.error(e)
        finally:
            cur.close()

    def MoveEntity(self,eid,etid):
        # changes meta entry's parent type
        # caller should update project tree
        logging.info("Entity move requested.")
        logging.info(eid)
        logging.info(etid)
        cur = self.conn.cursor()
        try:
            cur.execute("update entity set type=:tid where id=:eid;", \
                {'eid':eid,'tid':etid})
            self.conn.commit()
            ret=True
        except Exception as e:
            logging.error("Cannot move entity!")
            logging.error(e)
            ret=False
        finally:
            cur.close()
        return ret

    def DeleteEntity(self,eid):
        # deletes a metadata entry from the database
        # caller should update the project tree
        cur = self.conn.cursor()
        try:
            cur.execute("delete from entity_aliases where entity_id=:enid;",{'enid':eid})
            cur.execute("delete from related_entities where entity_id=:enid;",{'enid':eid})
            cur.execute("delete from related_entities where related_id=:enid;",{'enid':eid})
            cur.execute("delete from scene_entities where entity_id=:enid;",{'enid':eid})
            cur.execute("delete from entities where id=:enid;",{'enid':eid})
            self.conn.commit()
            ret = True
        except Exception as e:
            logging.error("Cannot delete entity!")
            logging.error(e)
            ret = False
        finally:
            cur.close()
        return ret

    def LinkEntity(self,eid,linktype,linkid):
        # links a metadata entry to either a scene or another entity
        # linktype = ['scene'|'meta']
        cur = self.conn.cursor()
        logging.info("Linking:")
        logging.info(eid)
        logging.info(linktype)
        logging.info(linkid)
        try:
            if linktype == 'Scene':
                logging.info("linking entity to scene")
                cur.execute("replace into scene_entities values (:sid, :eid);", \
                    {'sid':linkid,'eid':eid})
                self.conn.commit()
                ret = True
            elif linktype == 'Metadata Entry':
                logging.info("Linking entities")
                cur.execute("replace into related_entities values (:eid, :rid);", \
                    {'eid':eid,'rid':linkid})
                self.conn.commit()
                ret = True
            else:
                logging.warning("Invalid link type!")
                ret = False
        except Exception as e:
            logging.error("Cannot link entity in DB!")
            logging.error(e)
            ret = False
        finally:
                cur.close()
        return ret

    def IsLinked(self,eid,linktype,linkid):
        # checks DB to see if eid is linked to linkid
        cur = self.conn.cursor()
        try:
            if linktype == 'scene':
                logging.info("link type: entity to scene")
                cur.execute("""
                select * from scene_entities where scene_id=:scn and entity_id=:eid;
                """, {'scn':linkid,'eid':eid})
                if cur.fetchone() != None:
                    ret = True
                else:
                    ret = False
            elif linktype == 'meta':
                logging.info("Link type: entity to entity")
                cur.execute("""
                    select * from related_entities
                        where (entity_id=:eid and related_id=:relid)
                        or (entity_id=:relid and related_id=:eid);
                    """, {'relid':linkid,'eid':eid})
                if cur.fetchone() != None:
                    ret = True
                else:
                    ret = False
            else:
                logging.warning("Invalid link type!")
                ret = False
        except Exception as e:
            logging.error("Could not read database!")
            logging.error(e)
            ret = False
        finally:
            cur.close()
        return ret

    def GetProjectData(self):
        # returns a dictionary with project metadata
        #check:unverified
        logging.info("GetProjectData:")
        prj = {}
        cur = self.conn.cursor()
        cur.execute("select * from project where id=0;")
        r = cur.fetchone()
        prj['title']=r['title']
        prj['modified']=r['modified']
        prj['status']=r['editstatus']
        prj['path']=str(self.ppath)

        cur.close()
        logging.info(prj)
        return prj

    def GetSceneChapter(self,sid):
        # returns the parent chapter id of the given scene id
        #check:unverified
        logging.info("Scene_Chapter:")
        cur = self.conn.cursor()
        cur.execute("select chapter_id from chapter_scenes where scene_id=:scid;",{'scid':sid})
        cid = cur.fetchone()['chapter_id']
        cur.close()
        logging.info(cid)
        return cid

    def GetChapterBook(self,cid):
        # returns the parent book id of the given chapter id
        #check:unverified
        logging.info("Chapter_Book:")
        cur = self.conn.cursor()
        cur.execute("select book_id from book_chapters where chapter_id=:chid;",{'chid':cid})
        bid = cur.fetchone()['book_id']
        cur.close()
        logging.info(bid)
        return bid

    def GetSceneData(self,sceneid):
        # returns a dictionary with scene metadata for the given id
        # THIS DOES NOT INCLUDE CONTENTS
        # use OpenScene for that.
        # id, displayorder, title, contents, filepath, modified, editstatus
        #check:ok
        logging.info("Retrieving data for Scene %i." % sceneid)
        sdata = {}
        cur = self.conn.cursor()
        logging.info("Querying DB...")
        try:
            cur.execute("select title,displayorder,filepath,modified,editstatus,contents from scenes where id=:sid;", {"sid":sceneid})
        except Exception as e:
            logging.error("Error querying database:")
            logging.error(e)
        logging.info("Queried. Retrieving...")
        r = cur.fetchone()
        logging.info(dict(r))
        sdata['title'] = r['title']
        sdata['order'] = r['displayorder']
        sdata['file'] = r['filepath']
        sdata['modified'] = r['modified']
        sdata['status'] = r['editstatus']
        logging.info("Grabbing list of related IDs...")
        sdata['rel_ids'] = self.__GetSceneRelIDs(sceneid)
        logging.info("Done.")
        return sdata

    def GetEntityData(self,entityid):
        # returns a dictionary with entity metadata for the given id
        #check:unverified
        ent = {}
        try:
            logging.info("Querying for entity %i data..." % entityid)
            cur = self.conn.cursor()
            cur.execute("select name,desc,type from entities where id=:eid;",{'eid':entityid})
            r = cur.fetchone()
            if r != None:
                ent['name'] = r['name']
                ent['type'] = r['type']
                ent['desc'] = r['desc']
                ent['aliases'] = self.__GetAliases(entityid)
                if ent['aliases'] != None:
                    ent['alias_ids'] = map(self.__GetAliasID,ent['aliases'])
                else:
                    ent['alias_ids'] = None
                ent['related_ids'] = self.__GetERelIDs(entityid)
                if ent['related_ids'] != None:
                    ent['related_names'] = self.__GetERelNames(entityid)
                else:
                    ent['related_names'] = None
                logging.info(ent)
            else:
                logging.error("Could not retrieve entity data!")
                logging.error("Query returned no entity.")
                ent = None
        except Exception as err:
            logging.error("Could not retrieve entity data!")
            logging.error(err)
            ent = None
        finally:
            cur.close()
        return ent

    def GetEntityType(self,typeid):
        # returns a dict with singular, plural, and parent id
        #check:unverified
        et = {}
        logging.info("Retrieving type info...")
        cur = self.conn.cursor()
        cur.execute("select singular,plural,parent_id from entity_categories where id=:id;", {'id':typeid})
        r = cur.fetchone()
        if r != None:
            et['singular'] = r['singular']
            et['plural']=r['plural']
            et['parent']=r['parent_id']
            cur.close()
        else:
            et = None
        logging.info(et)
        return et

    def GetEntID(self,ename):
        # returns the ID of an entity given its name or alias
        # or None if not found
        #check:unverified
        logging.info("ID requested for entity %s" % ename)
        cur = self.conn.cursor()
        cur.execute("select id from entities where name=:en;",{'en':ename})
        r = cur.fetchone()
        if r == None:
            logging.info("No primary ID found.")
            cur.execute("select entity_id from entity_aliases where alias=:ename;",{'ename':ename})
            r = cur.fetchone()
            if r != None:
                eid = r['entity_id']
                logging.info(eid)
            else:
                logging.info("No matching aliases found.")
                eid = None
        else:
            eid = r['id']
            logging.info(eid)
        cur.close()
        return eid

    def __GetAliasID(self,aname):
        # returns the alias id given the alias string
        #check:unverified
        cur = self.conn.cursor()
        cur.execute("select alias_id from entity_aliases where alias = :aname;",{'aname':aname})
        r = cur.fetchone()
        if r != None:
            ret = r['alias_id']
        else:
            ret = None
        return ret

    def __GetAliases(self,eid):
        # returns a string of all aliases for the given entity id
        # one per line, seperated by '\n'
        #check:unverified
        alist = []
        cur = self.conn.cursor()
        cur.execute("select alias from entity_aliases where entity_id = :eid;",{'eid':eid})
        rows = cur.fetchall()
        if rows != []:
            for r in rows:
                alist.append(r['alias'])
        else:
            alist = None
        logging.info("Alias list:")
        logging.info(alist)
        return alist

    def __GetERelNames(self,eid):
        #check:unverified
        alist = []
        rels = self.__GetERelIDs(eid)
        if rels != None:
            for rid in rels:
                alist.append(self.GetEntityData(rid)['name'])
        else:
            alist = None
        logging.info("Relation names:")
        logging.info(alist)
        return alist

    def __GetERelIDs(self,eid):
        #check:unverified
        relids = []
        cur = self.conn.cursor()
        try:
            logging.info("Querying for related entity IDs...")
            cur.execute("select related_id from related_entities where entity_id=:enid;", {'enid':eid})
            logging.info("Query complete. Retrieving results.")
            results = cur.fetchall()
            logging.info(results)
            if results != []:
                for r in results:
                    logging.info("Entity Relation IDs:")
                    logging.info(dict(r))
                    relids.append(r['related_id'])
            else:
                logging.warning("Query returned no rows.")
                relids = None
        except Exception as e:
            logging.error("Error querying database:")
            logging.error(e)
            relids = None
        logging.info(relids)
        return relids

    def __GetSceneRelIDs(self,sid):
        # scene_entities (scene_id, entity_id)
        #check:ok
        logging.info("__GetSceneRelIDs called.")
        relids = []
        cur = self.conn.cursor()
        logging.info("Querying...")
        try:
            cur.execute("select entity_id from scene_entities where scene_id=:scnid;", {'scnid':sid})
            logging.info("Query complete. Retrieving results.")
            results = cur.fetchall()
            logging.info(results)
            if results != []:
                for r in results:
                    logging.info("Scene Relation IDs:")
                    logging.info(dict(r))
                    relids.append(r['entity_id'])
            else:
                logging.warning("Query returned no rows.")
                relids = None
        except Exception as e:
            logging.error("Error querying database:")
            logging.error(e)
            relids = None
        return relids
